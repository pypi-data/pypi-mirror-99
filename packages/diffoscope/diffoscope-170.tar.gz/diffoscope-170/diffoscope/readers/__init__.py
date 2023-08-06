#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2017 Ximin Luo <infinity0@debian.org>
# Copyright © 2017, 2020 Chris Lamb <lamby@debian.org>
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

import codecs

from diffoscope.utils import exit_if_paths_do_not_exist

from .json import JSONReaderV1


def load_diff_from_path(path):
    exit_if_paths_do_not_exist(path)
    with open(path, "rb") as fp:
        return load_diff(codecs.getreader("utf-8")(fp), path)


def load_diff(fp, path):
    return JSONReaderV1().load(fp, path)
