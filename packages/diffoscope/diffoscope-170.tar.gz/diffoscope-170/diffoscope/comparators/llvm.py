#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016 Ximin Luo <infinity0@debian.org>
# Copyright © 2016, 2018-2020 Chris Lamb <lamby@debian.org>
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

from diffoscope.tools import tool_required
from diffoscope.difference import Difference

from .utils.file import File
from .utils.command import Command


class LlvmBcAnalyzer(Command):
    @tool_required("llvm-bcanalyzer")
    def cmdline(self):
        return ["llvm-bcanalyzer", "-dump", self.path]

    def filter(self, line):
        if line.decode("utf-8", "ignore").startswith("Summary of "):
            return b"Summary:"
        return line


class LlvmBcDisassembler(Command):
    @tool_required("llvm-dis")
    def cmdline(self):
        # execute llvm-dis from the same directory as the file, so it doesn't
        # embed the whole path, including our tempdir, into the output.
        # this makes it easier to generate reproducible diffs for our tests.
        return [
            "find",
            self.path,
            "-execdir",
            "llvm-dis",
            "-o",
            "-",
            "{}",
            ";",
        ]


class LlvmBitCodeFile(File):
    DESCRIPTION = "LLVM IR bitcode files"
    FILE_TYPE_RE = re.compile(r"^LLVM IR bitcode")

    def compare_details(self, other, source=None):
        return [
            Difference.from_operation(LlvmBcAnalyzer, self.path, other.path),
            Difference.from_operation(
                LlvmBcDisassembler, self.path, other.path
            ),
        ]
