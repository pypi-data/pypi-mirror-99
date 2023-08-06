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

from diffoscope.tools import tool_required

from .utils.file import File
from .utils.archive import Archive

logger = logging.getLogger(__name__)


class Bzip2Container(Archive):
    def open_archive(self):
        return self

    def close_archive(self):
        pass

    def get_member_names(self):
        return [self.get_compressed_content_name(".bz2")]

    @tool_required("bzip2")
    def extract(self, member_name, dest_dir):
        dest_path = self.get_path_name(dest_dir)
        logger.debug("bzip2 extracting to %s", dest_path)
        with open(dest_path, "wb") as fp:
            subprocess.check_call(
                ["bzip2", "--decompress", "--stdout", self.source.path],
                stdout=fp,
                stderr=subprocess.PIPE,
            )
        return dest_path


class Bzip2File(File):
    DESCRIPTION = "bzip2 archives"
    CONTAINER_CLASSES = [Bzip2Container]
    FILE_TYPE_RE = re.compile(r"^bzip2 compressed data\b")
