#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2014-2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2015 Clemens Lang <cal@macports.org>
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

from diffoscope.tools import tool_required
from diffoscope.difference import Difference

from .utils.file import File
from .utils.command import Command, our_check_output


class Otool(Command):
    def __init__(self, path, arch, *args, **kwargs):
        self._path = path
        self._arch = arch
        super().__init__(path, *args, **kwargs)

    @tool_required("otool")
    def cmdline(self):
        return ["otool"] + self.otool_options() + [self.path]

    def otool_options(self):
        return ["-arch", self._arch]

    def filter(self, line):
        # Strip filename
        prefix = f"{self._path}:"
        if line.decode("utf-8", "ignore").startswith(prefix):
            return line[len(prefix) :].strip()
        return line


class OtoolHeaders(Otool):
    def otool_options(self):
        return super().otool_options() + ["-h"]


class OtoolLibraries(Otool):
    def otool_options(self):
        return super().otool_options() + ["-L"]


class OtoolDisassemble(Otool):
    def otool_options(self):
        return super().otool_options() + ["-tdvV"]


class OtoolDisassembleInternal(Otool):
    def otool_options(self):
        return super().otool_options() + ["-tdvVQ"]


class MachoFile(File):
    DESCRIPTION = "MacOS binaries"
    FILE_TYPE_RE = re.compile(r"^Mach-O ")
    RE_EXTRACT_ARCHS = re.compile(
        r"^(?:Architectures in the fat file: .* are|Non-fat file: .* is architecture): (.*)$"
    )

    @staticmethod
    @tool_required("lipo")
    def get_arch_from_macho(path):
        lipo_output = our_check_output(["lipo", "-info", path]).decode("utf-8")
        lipo_match = MachoFile.RE_EXTRACT_ARCHS.match(lipo_output)
        if lipo_match is None:
            raise ValueError(
                "lipo -info on Mach-O file %s did not produce expected output. Output was: %s"
                % path,
                lipo_output,
            )
        return lipo_match.group(1).split()

    def compare_details(self, other, source=None):
        differences = []
        # Check for fat binaries, trigger a difference if the architectures differ
        my_archs = MachoFile.get_arch_from_macho(self.path)
        other_archs = MachoFile.get_arch_from_macho(other.path)

        differences.append(
            Difference.from_text(
                "\n".join(my_archs),
                "\n".join(other_archs),
                self.name,
                other.name,
                source="architectures",
            )
        )

        # Compare common architectures for differences
        for common_arch in set(my_archs) & set(other_archs):
            differences.append(
                Difference.from_operation(
                    OtoolHeaders,
                    self.path,
                    other.path,
                    operation_args=[common_arch],
                    comment="Mach-O headers for architecture %s" % common_arch,
                )
            )
            differences.append(
                Difference.from_operation(
                    OtoolLibraries,
                    self.path,
                    other.path,
                    operation_args=[common_arch],
                    comment="Mach-O load commands for architecture %s"
                    % common_arch,
                )
            )

            x = Difference.from_operation(
                OtoolDisassemble,
                self.path,
                other.path,
                operation_args=[common_arch],
                comment="Code for architecture %s" % common_arch,
            )
            differences.append(x)

            # If the LLVM disassembler does not work, try the internal one.
            if x is None:
                differences.append(
                    Difference.from_operation(
                        OtoolDisassembleInternal,
                        self.path,
                        other.path,
                        operation_args=[common_arch],
                        comment="Code for architecture %s (internal disassembler)"
                        % common_arch,
                    )
                )

        return differences
