#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Daniel Kahn Gillmor <dkg@fifthhorseman.net>
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2015 Paul Gevers <elbrus@debian.org>
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

import os
import re
import logging
import subprocess

from diffoscope.tools import tool_required
from diffoscope.profiling import profile
from diffoscope.difference import Difference

from .utils.file import File
from .utils.command import Command, our_check_output

logger = logging.getLogger(__name__)


class Ppudump(Command):
    @tool_required("ppudump")
    def cmdline(self):
        return ["ppudump", self.path]

    def env(self):
        # ppudump will return times using the local timezone which is not ideal
        # to investigate files. TZ environment variable can be used to enforce UTC.
        # Currently there is no fpc release yet that includes the TC environment
        # variable, but it looks for timezone definitions in the directory
        # specified by TZDIR. So let's set it to a non-existent directory
        # so we get UTC output even when the system timezone is set otherwise.
        env = dict(os.environ)
        env["TZ"] = ":UTC"
        env["TZDIR"] = "/nonexistent"
        return env

    def filter(self, line):
        if re.match(
            r"^Analyzing %s \(v[0-9]+\)$" % re.escape(self.path),
            line.decode("utf-8", errors="ignore"),
        ):
            return b""
        return line


class PpuFile(File):
    DESCRIPTION = "FreePascal files (.ppu)"
    FILE_EXTENSION_SUFFIX = {".ppu"}

    @classmethod
    def recognizes(cls, file):
        if not super().recognizes(file):
            return False

        if not file.file_header.startswith(b"PPU"):
            return False

        ppu_version = file.file_header[3:6].decode("ascii", errors="ignore")

        if not hasattr(PpuFile, "ppu_version"):
            try:
                with profile("command", "ppudump"):
                    our_check_output(
                        ["ppudump", "-vh", file.path],
                        stderr=subprocess.STDOUT,
                    )
                PpuFile.ppu_version = ppu_version
            except subprocess.CalledProcessError as e:
                error = e.output.decode("utf-8", errors="ignore")
                m = re.search("Expecting PPU version ([0-9]+)", error)
                try:
                    PpuFile.ppu_version = m.group(1)
                except AttributeError:
                    if m is None:
                        PpuFile.ppu_version = None
                        logger.debug("Unable to read PPU version")
                    else:
                        raise
            except OSError:
                PpuFile.ppu_version = None
                logger.debug("Unable to read PPU version")

        if PpuFile.ppu_version != ppu_version:
            logger.debug(
                "ppudump version (%s) does not match header of %s (%s)",
                PpuFile.ppu_version,
                file.name,
                ppu_version,
            )
            return False

        return True

    def compare_details(self, other, source=None):
        return [Difference.from_operation(Ppudump, self.path, other.path)]
