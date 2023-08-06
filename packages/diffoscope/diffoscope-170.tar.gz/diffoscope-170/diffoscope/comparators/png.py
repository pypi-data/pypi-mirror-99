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
import logging
import subprocess

from diffoscope.config import Config
from diffoscope.tools import tool_required
from diffoscope.difference import Difference

from .image import pixel_difference, flicker_difference, same_size
from .utils.file import File
from .utils.command import Command

logger = logging.getLogger(__name__)


class Sng(Command):
    # sng will return 1 if there are even minor errors in the file
    VALID_RETURNCODES = {0, 1}

    @tool_required("sng")
    def cmdline(self):
        return ["sng"]

    def stdin(self):
        return open(self.path, "rb")


class PngFile(File):
    DESCRIPTION = "PNG images"
    FILE_TYPE_RE = re.compile(r"^PNG image data\b")

    def compare_details(self, other, source=None):
        sng_diff = Difference.from_operation(
            Sng, self.path, other.path, source="sng"
        )
        differences = [sng_diff]

        if (
            sng_diff is not None
            and Config().compute_visual_diffs
            and same_size(self, other)
        ):
            try:
                logger.debug(
                    "Generating visual difference for %s and %s",
                    self.path,
                    other.path,
                )
                content_diff = Difference(
                    None, self.path, other.path, source="Image content"
                )
                content_diff.add_visuals(
                    [
                        pixel_difference(self.path, other.path),
                        flicker_difference(self.path, other.path),
                    ]
                )
                differences.append(content_diff)
            except subprocess.CalledProcessError:  # noqa
                pass

        return differences
