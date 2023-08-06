#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
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


import time
import os.path
import ctypes
import logging
import libarchive
import collections

from diffoscope.exc import ContainerExtractionError
from diffoscope.config import Config
from diffoscope.excludes import any_excluded
from diffoscope.tempfiles import get_temporary_directory
from diffoscope.difference import Difference

from ..device import Device
from ..symlink import Symlink
from ..directory import Directory

from .archive import Archive, ArchiveMember

logger = logging.getLogger(__name__)


# Monkeypatch libarchive-c (<< 2.2)
if not hasattr(libarchive.ffi, "entry_rdevmajor"):
    libarchive.ffi.ffi(
        "entry_rdevmajor", [libarchive.ffi.c_archive_entry_p], ctypes.c_uint
    )
    libarchive.ArchiveEntry.rdevmajor = property(
        lambda self: libarchive.ffi.entry_rdevmajor(self._entry_p)
    )
if not hasattr(libarchive.ffi, "entry_rdevminor"):
    libarchive.ffi.ffi(
        "entry_rdevminor", [libarchive.ffi.c_archive_entry_p], ctypes.c_uint
    )
    libarchive.ArchiveEntry.rdevminor = property(
        lambda self: libarchive.ffi.entry_rdevminor(self._entry_p)
    )
# Monkeypatch libarchive-c (<< 2.3)
if not hasattr(libarchive.ffi, "entry_nlink"):
    libarchive.ffi.ffi(
        "entry_nlink", [libarchive.ffi.c_archive_entry_p], ctypes.c_uint
    )
    libarchive.ArchiveEntry.nlink = property(
        lambda self: libarchive.ffi.entry_nlink(self._entry_p)
    )
if not hasattr(libarchive.ffi, "entry_uid"):
    libarchive.ffi.ffi(
        "entry_uid", [libarchive.ffi.c_archive_entry_p], ctypes.c_uint32
    )
    libarchive.ArchiveEntry.uid = property(
        lambda self: libarchive.ffi.entry_uid(self._entry_p)
    )
if not hasattr(libarchive.ffi, "entry_gid"):
    libarchive.ffi.ffi(
        "entry_gid", [libarchive.ffi.c_archive_entry_p], ctypes.c_uint32
    )
    libarchive.ArchiveEntry.gid = property(
        lambda self: libarchive.ffi.entry_uid(self._entry_p)
    )
if not hasattr(libarchive.ffi, "entry_mtime_nsec"):
    libarchive.ffi.ffi(
        "entry_mtime_nsec", [libarchive.ffi.c_archive_entry_p], ctypes.c_long
    )
    libarchive.ArchiveEntry.mtime_nsec = property(
        lambda self: libarchive.ffi.entry_mtime_nsec(self._entry_p)
    )
if not hasattr(libarchive.ffi, "entry_uname"):
    libarchive.ffi.ffi(
        "entry_uname", [libarchive.ffi.c_archive_entry_p], ctypes.c_char_p
    )
    libarchive.ArchiveEntry.uname = property(
        lambda self: libarchive.ffi.entry_uname(self._entry_p)
    )
if not hasattr(libarchive.ffi, "entry_gname"):
    libarchive.ffi.ffi(
        "entry_gname", [libarchive.ffi.c_archive_entry_p], ctypes.c_char_p
    )
    libarchive.ArchiveEntry.gname = property(
        lambda self: libarchive.ffi.entry_gname(self._entry_p)
    )
# Monkeypatch libarchive-c (>= 2.8)
# Wire mtime_nsec attribute as some libarchive versions (>=2.8) don't expose it
# for ArchiveEntry. Doing this allows a unified API no matter which version is
# available.
if not hasattr(libarchive.ArchiveEntry, "mtime_nsec") and hasattr(
    libarchive.ffi, "entry_mtime_nsec"
):
    libarchive.ArchiveEntry.mtime_nsec = property(
        lambda self: libarchive.ffi.entry_mtime_nsec(self._entry_p)
    )


# Monkeypatch libarchive-c so we always get pathname as (Unicode) str
# Otherwise, we'll get sometimes str and sometimes bytes and always pain.
libarchive.ArchiveEntry.pathname = property(
    lambda self: libarchive.ffi.entry_pathname(self._entry_p).decode(
        "utf-8", errors="surrogateescape"
    )
)


def list_libarchive(path, ignore_errors=False):
    try:
        with libarchive.file_reader(path) as archive:
            for entry in archive:
                name_and_link = entry.name
                if entry.issym:
                    name_and_link = "{entry.name} -> {entry.linkname}".format(
                        entry=entry
                    )
                if Config().exclude_directory_metadata == "recursive":
                    yield "{name_and_link}\n".format(
                        name_and_link=name_and_link
                    )
                    continue
                if entry.isblk or entry.ischr:
                    size_or_dev = "{major:>3},{minor:>3}".format(
                        major=entry.rdevmajor, minor=entry.rdevminor
                    )
                else:
                    size_or_dev = "-" if entry.size is None else entry.size
                mtime = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.gmtime(entry.mtime)
                ) + ".{:06d}".format(entry.mtime_nsec // 1000)
                if entry.uname:
                    user = "{user:<8} {uid:>7}".format(
                        user=entry.uname.decode(
                            "utf-8", errors="surrogateescape"
                        ),
                        uid="({})".format(entry.uid),
                    )
                else:
                    user = entry.uid
                if entry.gname:
                    group = "{group:<8} {gid:>7}".format(
                        group=entry.gname.decode(
                            "utf-8", errors="surrogateescape"
                        ),
                        gid="({})".format(entry.gid),
                    )
                else:
                    group = entry.gid
                yield "{strmode} {entry.nlink:>3} {user:>8} {group:>8} {size_or_dev:>8} {mtime:>8} {name_and_link}\n".format(
                    strmode=entry.strmode.decode("us-ascii"),
                    entry=entry,
                    user=user,
                    group=group,
                    size_or_dev=size_or_dev,
                    mtime=mtime,
                    name_and_link=name_and_link,
                )
    except libarchive.exception.ArchiveError:
        if not ignore_errors:
            raise


class LibarchiveMember(ArchiveMember):
    def __init__(self, archive, entry):
        super().__init__(archive, entry.pathname)

    def is_directory(self):
        return False

    def is_symlink(self):
        return False

    def is_device(self):
        return False


class LibarchiveDirectory(Directory, LibarchiveMember):
    def __init__(self, archive, entry):
        LibarchiveMember.__init__(self, archive, entry)

    def compare(self, other, source=None):
        return None

    def has_same_content_as(self, other):
        return False

    @property
    def path(self):
        raise NotImplementedError(
            "LibarchiveDirectory is not meant to be extracted."
        )

    def is_directory(self):
        return True

    def get_member_names(self):
        raise ValueError("archives are compared as a whole.")  # noqa

    def get_member(self, member_name):
        raise ValueError("archives are compared as a whole.")  # noqa


class LibarchiveSymlink(Symlink, LibarchiveMember):
    def __init__(self, archive, entry):
        LibarchiveMember.__init__(self, archive, entry)
        self._destination = entry.linkpath

    @property
    def symlink_destination(self):
        return self._destination

    def is_symlink(self):
        return True


class LibarchiveDevice(Device, LibarchiveMember):
    def __init__(self, container, entry):
        LibarchiveMember.__init__(self, container, entry)
        self._mode = entry.mode
        self._major = entry.rdevmajor
        self._minor = entry.rdevminor

    def get_device(self):
        return (self._mode, self._major, self._minor)

    def is_device(self):
        return True


class LibarchiveContainer(Archive):
    def open_archive(self):
        # libarchive is very very stream oriented an not for random access
        # so we are going to reopen the archive everytime
        # not nice, but it'll work
        return True

    def close_archive(self):
        pass

    def get_member_names(self):
        self.ensure_unpacked()
        return self._members.keys()

    def get_member(self, member_name):
        with libarchive.file_reader(self.source.path) as archive:
            for entry in archive:
                if entry.pathname == member_name:
                    return self.get_subclass(entry)
        raise KeyError("%s not found in archive" % member_name)

    def get_filtered_members(self):
        try:
            with libarchive.file_reader(self.source.path) as archive:
                for entry in archive:
                    if any_excluded(entry.pathname):
                        continue
                    yield entry.pathname, self.get_subclass(entry)
        except libarchive.exception.ArchiveError:
            pass

    def extract(self, member_name, dest_dir):
        self.ensure_unpacked()
        return self._members[member_name]

    def get_subclass(self, entry):
        if entry.isdir:
            return LibarchiveDirectory(self, entry)
        if entry.issym:
            return LibarchiveSymlink(self, entry)
        if entry.isblk or entry.ischr:
            return LibarchiveDevice(self, entry)

        return LibarchiveMember(self, entry)

    def ensure_unpacked(self):
        if hasattr(self, "_members"):
            return

        self._tmpdir_object = get_temporary_directory(
            suffix=self.__class__.__name__
        )
        tmpdir = self._tmpdir_object.name
        self._members = collections.OrderedDict()

        logger.debug("Extracting %s to %s", self.source.path, tmpdir)

        with libarchive.file_reader(self.source.path) as archive:
            for idx, entry in enumerate(archive):
                # Always skip directories
                if entry.isdir:
                    continue

                # Don't extract excluded files
                if any_excluded(entry.pathname):
                    continue

                # Keep directory sizes small. could be improved but should be
                # good enough for "ordinary" large archives.
                dst = os.path.join(tmpdir, str(idx // 4096), str(idx % 4096))
                _, ext = os.path.splitext(entry.pathname)
                dst += ext

                # Maintain a mapping of archive path to the extracted path,
                # avoiding the need to sanitise filenames.
                self._members[entry.pathname] = dst

                logger.debug("Extracting %s to %s", entry.pathname, dst)

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                try:
                    with open(dst, "wb") as f:
                        for block in entry.get_blocks(block_size=2 ** 17):
                            f.write(block)
                except Exception as e:
                    raise ContainerExtractionError(entry.pathname, e)

        logger.debug(
            "Extracted %d entries from %s to %s",
            len(self._members),
            self.source.path,
            tmpdir,
        )

    def comparisons(self, other):
        def hide_trivial_dirs(item):
            file1, file2, comment = item
            return not (
                isinstance(file1, Directory)
                and isinstance(file2, Directory)
                and comment is None
            )

        return filter(hide_trivial_dirs, super().comparisons(other))


class LibarchiveContainerWithFilelist(LibarchiveContainer):
    def compare(self, other, **kwargs):
        differences = []

        # Always include the filelist
        if other.source:
            differences = [
                Difference.from_text_readers(
                    list_libarchive(self.source.path),
                    list_libarchive(other.source.path),
                    self.source.path,
                    other.source.path,
                    source="file list",
                )
            ]

        differences.extend(super().compare(other, **kwargs))

        return differences
