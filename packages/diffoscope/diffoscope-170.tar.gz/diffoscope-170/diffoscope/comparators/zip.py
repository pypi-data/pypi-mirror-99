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

import re
import sys
import shutil
import os.path
import zipfile

from diffoscope.config import Config
from diffoscope.tools import tool_required
from diffoscope.difference import Difference
from diffoscope.exc import ContainerExtractionError, RequiredToolNotFound
from diffoscope.tempfiles import get_named_temporary_file

from .utils.file import File
from .directory import Directory
from .utils.archive import Archive, ArchiveMember
from .utils.command import Command


class Zipinfo(Command):
    # zipinfo returns with an exit code of 1 or 2 when reading
    # Mozilla-optimized or Java "jmod" ZIPs as they have non-standard headers
    # which are safe to ignore.
    VALID_RETURNCODES = {0, 1, 2}

    re_strip_path = re.compile(r"^(warning|error) \[[^\]]+\]:\s+(.*)$")

    @tool_required("zipinfo")
    def cmdline(self):
        return ["zipinfo", self.path]

    def filter(self, line):
        # we don't care about the archive file path
        if line.startswith(b"Archive:"):
            return b""

        # Strip paths from errors and warnings
        # eg: "warning [/full/path]: 472 extra bytes at beginning or within zipfile"
        m = self.re_strip_path.match(line.decode("utf-8"))
        if m is not None:
            return "{}: {}\n".format(m.group(1), m.group(2)).encode("utf-8")

        return line


class ZipinfoVerbose(Zipinfo):
    @tool_required("zipinfo")
    def cmdline(self):
        return ["zipinfo", "-v", self.path]


class Zipnote(Command):
    # zipnote returns with an exit code of 3 for invalid archives
    VALID_RETURNCODES = {0, 3}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.flag = False

    @tool_required("zipnote")
    def cmdline(self):
        path = self.path
        if not path.endswith(".zip"):
            path = get_named_temporary_file(suffix=".zip").name
            shutil.copy(self.path, path)
        return ["zipnote", path]

    def filter(self, line):
        """
        Example output from zipnote(1):

            @ foo
            hello
            @ (comment above this line)
            @ (zip file comment below this line)
            goodbye
        """

        if line == b"@ (zip file comment below this line)\n":
            self.flag = True
            return b"Zip file comment: "

        if line == b"@ (comment above this line)\n":
            self.flag = False
            return b"\n\n"  # spacer

        if line.startswith(b"@ "):
            filename = line[2:-1].decode()
            self.flag = True
            return f"Filename: {filename}\nComment: ".encode()

        return line[:-1] if self.flag else b""


class BsdtarVerbose(Command):
    @tool_required("bsdtar")
    def cmdline(self):
        return ["bsdtar", "-tvf", self.path]


def zipinfo_differences(file, other):
    """
    Run all our zipinfo variants.
    """

    for x in (Zipinfo, ZipinfoVerbose, BsdtarVerbose):
        result = Difference.from_operation(x, file.path, other.path)
        # We only return the 'best' one
        if result is not None:
            return [result]

    return []


class ZipDirectory(Directory, ArchiveMember):
    def __init__(self, archive, member_name):
        ArchiveMember.__init__(self, archive, member_name)

    def compare(self, other, source=None):
        return None

    def has_same_content_as(self, other):
        return False

    def is_directory(self):
        return True

    def get_member_names(self):
        raise ValueError("Zip archives are compared as a whole.")  # noqa

    def get_member(self, member_name):
        raise ValueError("Zip archives are compared as a whole.")  # noqa


class ZipContainer(Archive):
    def open_archive(self):
        return zipfile.ZipFile(self.source.path, "r")

    def close_archive(self):
        self.archive.close()

    def get_member_names(self):
        return self.archive.namelist()

    def extract(self, member_name, dest_dir):
        # We don't really want to crash if the filename in the zip archive
        # can't be encoded using the filesystem encoding. So let's replace
        # any weird character so we can get to the bytes.
        targetpath = os.path.join(
            dest_dir, os.path.basename(member_name)
        ).encode(sys.getfilesystemencoding(), errors="replace")

        try:
            with self.archive.open(member_name) as source, open(
                targetpath, "wb"
            ) as target:
                shutil.copyfileobj(source, target)
            return targetpath.decode(sys.getfilesystemencoding())
        except RuntimeError as e:
            # Handle encrypted files see line 1292 of zipfile.py
            is_encrypted = self.archive.getinfo(member_name).flag_bits & 0x1
            if is_encrypted:
                raise ContainerExtractionError(member_name, e)
            raise

    def get_member(self, member_name):
        zipinfo = self.archive.getinfo(member_name)
        if zipinfo.filename[-1] == "/":
            return ZipDirectory(self, member_name)
        return ArchiveMember(self, member_name)


class ZipFile(File):
    DESCRIPTION = "ZIP archives"
    CONTAINER_CLASSES = [ZipContainer]
    FILE_TYPE_RE = re.compile(
        r"^((?:iOS App )?Zip archive|Java archive|EPUB document|OpenDocument (Text|Spreadsheet|Presentation|Drawing|Formula|Template|Text Template)|Google Chrome extension)\b"
    )

    def compare_details(self, other, source=None):
        differences = []
        if Config().exclude_directory_metadata != "recursive":
            differences.extend(zipinfo_differences(self, other))

        try:
            differences.append(
                Difference.from_operation(Zipnote, self.path, other.path)
            )
        except RequiredToolNotFound:  # noqa
            pass

        return differences


class MozillaZipContainer(ZipContainer):
    def open_archive(self):
        # This is gross: Monkeypatch zipfile._EndRecData to work with
        # Mozilla-optimized ZIPs
        _orig_EndRecData = zipfile._EndRecData

        def _EndRecData(fh):
            endrec = _orig_EndRecData(fh)
            if endrec:
                endrec[zipfile._ECD_LOCATION] = (
                    endrec[zipfile._ECD_OFFSET] + endrec[zipfile._ECD_SIZE]
                )
            return endrec

        zipfile._EndRecData = _EndRecData
        result = super(MozillaZipContainer, self).open_archive()
        zipfile._EndRecData = _orig_EndRecData
        return result


class MozillaZipFile(ZipFile):
    DESCRIPTION = "Mozilla-optimized .ZIP archives"
    CONTAINER_CLASSES = [MozillaZipContainer]

    @classmethod
    def recognizes(cls, file):
        # Mozilla-optimized ZIPs start with a 32-bit little endian integer
        # indicating the amount of data to preload, followed by the ZIP
        # central directory (with a PK\x01\x02 signature)
        return file.file_header[4:8] == b"PK\x01\x02"


class JmodJavaModule(ZipFile):
    DESCRIPTION = "Java .jmod modules"
    FILE_TYPE_RE = re.compile(r"^(Zip archive data|Java jmod module)")

    @classmethod
    def recognizes(cls, file):
        # Not all versions of file(1) support the detection of these
        # modules yet so we perform our own manual check for a "JM" prefix.
        return file.file_header[:2] == b"JM"
