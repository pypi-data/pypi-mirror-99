#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015      Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016-2017 Mattia Rizzolo <mattia@debian.org>
# Copyright © 2019-2020 Chris Lamb <lamby@debian.org>
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

import contextlib
import os
import re
import pytest

from diffoscope.comparators.binary import FilesystemFile
from diffoscope.comparators.utils.specialize import specialize

re_normalize_zeros = re.compile(
    r"^(?P<prefix>[ \-\+])(?P<offset>[0-9a-f]+)(?=: )", re.MULTILINE
)


def init_fixture(filename):
    return pytest.fixture(lambda: specialize(FilesystemFile(filename)))


def data(filename):
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", filename
    )


def get_data(filename):
    with open(data(filename), encoding="utf-8") as f:
        return f.read()


def assert_diff(difference, filename):
    assert difference.unified_diff == get_data(filename)


# https://code.activestate.com/recipes/576620-changedirectory-context-manager/#c3
@contextlib.contextmanager
def cwd_data():
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = os.getcwd()
    os.chdir(data(""))
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def load_fixture(filename):
    return init_fixture(data(filename))


def normalize_zeros(s):
    # older xxd had one zero less.  Make sure there are always 8.
    def repl(x):
        return "{}{:08x}".format(x.group("prefix"), int(x.group("offset"), 16))

    return re_normalize_zeros.sub(repl, s)
