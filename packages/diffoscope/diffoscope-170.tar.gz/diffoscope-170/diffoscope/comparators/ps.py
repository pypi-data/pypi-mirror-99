#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2016 Reiner Herrmann <reiner@reiner-h.de>
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
import logging

from diffoscope.exc import RequiredToolNotFound
from diffoscope.tools import tool_required
from diffoscope.difference import Difference

from .text import TextFile
from .utils.command import Command

logger = logging.getLogger(__name__)


class Pstotext(Command):
    @tool_required("ps2ascii")
    def cmdline(self):
        return ["ps2ascii", self.path]


class PsFile(TextFile):
    DESCRIPTION = "PostScript documents"
    FILE_TYPE_RE = re.compile(r"^PostScript document\b")

    def compare(self, other, *args, **kwargs):
        differences = super().compare(other, *args, **kwargs)
        details = None
        try:
            details = Difference.from_operation(
                Pstotext, self.path, other.path
            )
        except RequiredToolNotFound:  # noqa
            logger.debug("ps2ascii not found")

        if details:
            differences.add_details([details])
        return differences
