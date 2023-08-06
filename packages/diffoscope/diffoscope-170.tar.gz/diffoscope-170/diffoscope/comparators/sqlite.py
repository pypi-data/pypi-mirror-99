#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016-2018, 2020 Chris Lamb <lamby@debian.org>
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


class Sqlite3Dump(Command):
    @tool_required("sqlite3")
    def cmdline(self):
        return ["sqlite3", self.path, ".dump"]


class Sqlite3Database(File):
    DESCRIPTION = "SQLite databases"
    FILE_TYPE_RE = re.compile(r"^SQLite 3.x database")

    def compare_details(self, other, source=None):
        return [Difference.from_operation(Sqlite3Dump, self.path, other.path)]
