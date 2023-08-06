#
# diffoscope: in-depth comparison of files, archives, and directories
#
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

import io
import os
import shlex
import logging
import binascii
import subprocess

from diffoscope.tools import tool_required
from diffoscope.exc import RequiredToolNotFound
from diffoscope.utils import exit_if_paths_do_not_exist
from diffoscope.config import Config
from diffoscope.excludes import any_excluded
from diffoscope.profiling import profile
from diffoscope.difference import Difference

from ..missing_file import MissingFile

from .command import Command
from .specialize import specialize


logger = logging.getLogger(__name__)


class Xxd(Command):
    @tool_required("xxd")
    def cmdline(self):
        return ["xxd", self.path]


def compare_root_paths(path1, path2):
    from ..directory import (
        FilesystemDirectory,
        FilesystemFile,
        compare_directories,
        compare_meta,
    )

    if not Config().new_file:
        exit_if_paths_do_not_exist(path1, path2)
    if any_excluded(path1, path2):
        return None

    if os.path.isdir(path1) and os.path.isdir(path2):
        return compare_directories(path1, path2)

    container1 = FilesystemDirectory(os.path.dirname(path1)).as_container
    file1 = specialize(FilesystemFile(path1, container=container1))
    container2 = FilesystemDirectory(os.path.dirname(path2)).as_container
    file2 = specialize(FilesystemFile(path2, container=container2))
    difference = compare_files(file1, file2)

    if Config().exclude_directory_metadata in ("no", "recursive"):
        meta = compare_meta(path1, path2)
        if meta:
            # Create an "empty" difference so we have something to attach file
            # metadata to.
            if difference is None:
                difference = Difference(None, file1.name, file2.name)
            difference.add_details(meta)
    return difference


def compare_files(file1, file2, source=None, diff_content_only=False):
    logger.debug(
        "Comparing %s (%s) and %s (%s)",
        file1.name or "-",
        file1.__class__.__name__,
        file2.name or "-",
        file2.__class__.__name__,
    )

    if any_excluded(file1.name, file2.name):
        return None

    # Specialize the files first so "has_same_content_as" can be overridden
    # by subclasses
    specialize(file1)
    specialize(file2)

    force_details = Config().force_details
    with profile("has_same_content_as", file1):
        has_same_content = file1.has_same_content_as(file2)

    if has_same_content:
        if not force_details:
            logger.debug(
                "has_same_content_as returned True; skipping further comparisons"
            )
            return None
        if diff_content_only:
            return None
    elif diff_content_only:
        return Difference(None, file1.name, file2.name, comment="Files differ")

    call_difftool(file1, file2)

    if isinstance(file1, MissingFile):
        file1.other_file = file2
    elif isinstance(file2, MissingFile):
        file2.other_file = file1
    elif (file1.__class__.__name__ != file2.__class__.__name__) and (
        file1.as_container is None or file2.as_container is None
    ):
        return file1.compare_bytes(file2, source)
    with profile("compare_files (cumulative)", file1):
        return file1.compare(file2, source)


def call_difftool(file1, file2):
    """
    Call an external difftool one-by-one, similar to git-difftool(1).
    """

    if Config().difftool is None:
        return

    a = "/dev/null" if isinstance(file1, MissingFile) else file1.path
    b = "/dev/null" if isinstance(file2, MissingFile) else file2.path

    if os.path.isdir(a) or os.path.isdir(b):
        return

    cmd = " ".join((Config().difftool, shlex.quote(a), shlex.quote(b)))
    logger.debug("Calling external command: %s", " ".join(cmd))
    subprocess.call(cmd, shell=True)


def compare_binary_files(file1, file2, source=None):
    try:
        if source is None:
            source = [file1.name, file2.name]
        return Difference.from_operation(
            Xxd,
            file1.path,
            file2.path,
            source=source,
            has_internal_linenos=True,
        )
    except RequiredToolNotFound:
        hexdump1 = hexdump_fallback(file1.path)
        hexdump2 = hexdump_fallback(file2.path)
        comment = (
            "xxd not available in path. Falling back to Python hexlify.\n"
        )
        return Difference.from_text(
            hexdump1, hexdump2, file1.name, file2.name, source, comment
        )


def hexdump_fallback(path):
    hexdump = io.StringIO()
    with open(path, "rb") as f:
        for buf in iter(lambda: f.read(32), b""):
            hexdump.write("%s\n" % binascii.hexlify(buf).decode("us-ascii"))
    return hexdump.getvalue()
