#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
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

from .utils.file import File


class AbstractRpmFile(File):
    FILE_TYPE_RE = re.compile(r"^RPM\s")


class RpmFile(AbstractRpmFile):
    def compare(self, other, source=None):
        difference = self.compare_bytes(other)
        if not difference:
            return None
        difference.add_comment(
            "Unable to import Python rpm module. Falling back to binary comparison."
        )
        return difference
