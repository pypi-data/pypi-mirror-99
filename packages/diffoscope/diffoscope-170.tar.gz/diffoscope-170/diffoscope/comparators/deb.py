#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2014-2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2015-2020 Chris Lamb <lamby@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
import logging

from diffoscope.config import Config
from diffoscope.difference import Difference
from diffoscope.tools import python_module_missing

from .tar import TarContainer
from .utils.compare import compare_files
from .utils.file import File
from .utils.archive import ArchiveMember
from .utils.libarchive import LibarchiveContainer, list_libarchive
from .utils.specialize import specialize

try:
    from debian import deb822
except ImportError:
    python_module_missing("debian")
    deb822 = None

logger = logging.getLogger(__name__)


# Return a dict with build ids as keys and file as values for all deb in the
# given container
def get_build_id_map(container):
    d = {}
    for member_name, member in container.get_adjusted_members():
        # Let's assume the name will end with .deb to avoid looking at
        # too many irrelevant files
        if not member_name.endswith(".deb"):
            continue

        specialize(member)

        if isinstance(member, DebFile) and member.control:
            build_ids = member.control.get("Build-Ids", None)
            if build_ids:
                d.update({build_id: member for build_id in build_ids.split()})

    return d


class DebContainer(LibarchiveContainer):
    RE_DATA_TAR = re.compile(r"^data\.tar(\.gz|\.xz|\.bz2|\.lzma)?$")
    RE_CONTROL_TAR = re.compile(r"^control\.tar(\.gz|\.xz)?$")

    @property
    def data_tar(self):
        for name, member in self.get_adjusted_members():
            if not DebContainer.RE_DATA_TAR.match(name):
                continue

            specialize(member)

            if name.endswith(".tar"):
                return member

            return specialize(member.as_container.get_member("content"))

    @property
    def control_tar(self):
        for name, member in self.get_adjusted_members():
            if not DebContainer.RE_CONTROL_TAR.match(name):
                continue

            specialize(member)

            if name.endswith(".tar"):
                return member

            return specialize(member.as_container.get_member("content"))

    def perform_fuzzy_matching(self, my_members, other_members):
        matched = set()

        # Create local copies because they will be modified by consumer
        my_members = dict(my_members)
        other_members = dict(other_members)

        for name1 in my_members.keys():
            main, _ = os.path.splitext(name1)
            candidates = [
                name2
                for name2 in other_members.keys() - matched
                if os.path.splitext(name2)[0] == main
            ]
            if len(candidates) == 1:
                yield name1, candidates[0], 0
                matched.add(candidates[0])


class DebFile(File):
    CONTAINER_CLASSES = [DebContainer]
    FILE_TYPE_RE = re.compile(r"^Debian binary package")

    @property
    def md5sums(self):
        if not hasattr(self, "_md5sums"):
            control_tar = self.as_container.control_tar
            md5sums_file = (
                control_tar.as_container.lookup_file("./md5sums")
                if control_tar
                else None
            )
            if isinstance(md5sums_file, Md5sumsFile):
                self._md5sums = md5sums_file.parse()
            else:
                logger.debug("Unable to find a md5sums file")
                self._md5sums = {}
        return self._md5sums

    @property
    def control(self):
        if not deb822:
            return None

        if not hasattr(self, "_control"):
            control_file = (
                self.as_container.control_tar.as_container.lookup_file(
                    "./control"
                )
            )
            if control_file:
                with open(control_file.path, "rb") as f:
                    self._control = deb822.Deb822(f)

        return self._control

    def compare_details(self, other, source=None):
        return [
            Difference.from_text_readers(
                list_libarchive(self.path),
                list_libarchive(other.path),
                self.path,
                other.path,
                source="file list",
            )
        ]


class Md5sumsFile(File):
    @classmethod
    def recognizes(cls, file):
        return (
            isinstance(file, ArchiveMember)
            and file.name == "./md5sums"
            and isinstance(file.container.source, ArchiveMember)
            and isinstance(
                file.container.source.container.source, ArchiveMember
            )
            and DebContainer.RE_CONTROL_TAR.match(
                file.container.source.container.source.name
            )
            and isinstance(
                file.container.source.container.source.container.source,
                DebFile,
            )
        )

    def parse(self):
        try:
            md5sums = {}
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    md5sum, path = re.split(r"\s+", line.strip(), maxsplit=1)
                    md5sums["./%s" % path] = md5sum
            return md5sums
        except (UnicodeDecodeError, ValueError):
            logger.debug("Malformed md5sums, ignoring.")
            return {}

    def strip_checksum(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                yield " ".join(line.split(" ")[2:])

    def compare_details(self, other, source=None):
        return [
            compare_files(
                self, other, source="md5sums", diff_content_only=True
            ),
            Difference.from_text_readers(
                self.strip_checksum(self.path),
                self.strip_checksum(other.path),
                self.path,
                other.path,
                source="line order",
            ),
        ]


class DebTarContainer(TarContainer):
    def comparisons(self, other):
        my_md5sums = {}
        other_md5sums = {}

        if self.source:
            my_md5sums = self.source.container.source.container.source.md5sums
        if other.source:
            other_md5sums = (
                other.source.container.source.container.source.md5sums
            )

        for my_member, other_member, comment in super().comparisons(other):
            if (
                not Config().force_details
                and my_member.name == other_member.name
                and my_md5sums.get(my_member.name, "my")
                == other_md5sums.get(other_member.name, "other")
            ):
                logger.debug("Skipping %s: identical md5sum", my_member.name)
                continue
            yield my_member, other_member, comment


class DebDataTarFile(File):
    CONTAINER_CLASSES = [DebTarContainer]

    @classmethod
    def recognizes(cls, file):
        return (
            isinstance(file, ArchiveMember)
            and isinstance(file.container.source, ArchiveMember)
            and DebContainer.RE_DATA_TAR.match(file.container.source.name)
            and isinstance(file.container.source.container.source, DebFile)
        )

    def compare_details(self, other, source=None):
        return [
            Difference.from_text_readers(
                list_libarchive(self.path, ignore_errors=True),
                list_libarchive(other.path, ignore_errors=True),
                self.path,
                other.path,
                source="file list",
            )
        ]
