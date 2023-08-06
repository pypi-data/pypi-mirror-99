#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Reiner Herrmann <reiner@reiner-h.de>
# Copyright © 2016-2020 Chris Lamb <lamby@debian.org>
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
import logging
import os.path

from diffoscope.difference import Difference
from diffoscope.tools import python_module_missing
from diffoscope.profiling import profile

from .utils.file import File
from .utils.archive import Archive

try:
    import guestfs
except ImportError:
    python_module_missing("guestfs")
    guestfs = None

logger = logging.getLogger(__name__)


class FsImageContainer(Archive):
    def open_archive(self):
        if not guestfs:
            return None

        self.g = guestfs.GuestFS(python_return_dict=True)
        try:
            # force a check that LIBGUESTFS_CACHEDIR exists. otherwise guestfs
            # will fall back to /var/tmp, which we don't want
            self.g.set_cachedir(os.environ["LIBGUESTFS_CACHEDIR"])
        except KeyError:
            pass
        self.g.add_drive_opts(self.source.path, format="raw", readonly=1)
        try:
            logger.debug("Launching guestfs; this may take some time")
            with profile("command", "guestfs"):
                self.g.launch()
            logger.debug("guestfs successful launched")
        except RuntimeError:
            logger.exception("guestfs failed to launch")
            logger.error(
                "If memory is too tight for 512 MiB, try running "
                "with LIBGUESTFS_MEMSIZE=256 or lower."
            )
            return None
        devices = self.g.list_devices()
        try:
            self.g.mount_options("ro", devices[0], "/")
        except RuntimeError:
            logger.exception("guestfs count not mount image; invalid file?")
            return None
        self.fs = self.g.list_filesystems()[devices[0]]
        return self

    def close_archive(self):
        if not guestfs:
            return None

        try:
            self.g.umount_all()
            self.g.close()
        except Exception:  # noqa
            pass

    def get_member_names(self):
        if not guestfs:
            return []
        return [os.path.basename(self.source.path) + ".tar"]

    def extract(self, member_name, dest_dir):
        dest_path = os.path.join(dest_dir, member_name)
        logger.debug("filesystem image extracting to %s", dest_path)
        self.g.tar_out("/", dest_path)
        return dest_path


class FsImageFile(File):
    DESCRIPTION = "ext2/ext3/ext4/btrfs/fat filesystems"
    CONTAINER_CLASSES = [FsImageContainer]
    FILE_TYPE_RE = re.compile(
        r"^(Linux.*filesystem data|BTRFS Filesystem|F2FS filesystem).*"
    )

    @classmethod
    def recognizes(cls, file):
        # Avoid DOS / MBR file type as it generate a lot of false positives,
        # manually check "System identifier string" instead
        with open(file.path, "rb") as f:
            f.seek(54)
            if f.read(8) in (b"FAT12   ", b"FAT16   "):
                return True
            f.seek(82)
            if f.read(8) == b"FAT32   ":
                return True
        return super().recognizes(file)

    def compare_details(self, other, source=None):
        differences = []
        my_fs = ""
        other_fs = ""
        if hasattr(self.as_container, "fs"):
            my_fs = self.as_container.fs
        if hasattr(other.as_container, "fs"):
            other_fs = other.as_container.fs
        if my_fs != other_fs:
            differences.append(
                Difference.from_text(
                    my_fs, other_fs, None, None, source="filesystem"
                )
            )
        if not guestfs:
            self.add_comment(
                "Installing the 'guestfs' package may produce a better output."
            )
        return differences
