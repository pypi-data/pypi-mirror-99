#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
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

import pytest

from diffoscope.comparators.sqlite import Sqlite3Database

from ..utils.data import load_fixture, get_data
from ..utils.tools import skip_unless_tools_exist
from ..utils.nonexisting import assert_non_existing


sqlite3db1 = load_fixture("test1.sqlite3")
sqlite3db2 = load_fixture("test2.sqlite3")


def test_identification(sqlite3db1):
    assert isinstance(sqlite3db1, Sqlite3Database)


def test_no_differences(sqlite3db1):
    difference = sqlite3db1.compare(sqlite3db1)
    assert difference is None


@pytest.fixture
def differences(sqlite3db1, sqlite3db2):
    return sqlite3db1.compare(sqlite3db2).details


@skip_unless_tools_exist("sqlite3")
def test_diff(differences):
    expected_diff = get_data("sqlite3_expected_diff")
    actual_diff = differences[0].unified_diff
    assert (
        actual_diff == expected_diff
        or actual_diff == expected_diff.replace('"test"', "test")
    )


@skip_unless_tools_exist("sqlite3")
def test_compare_non_existing(monkeypatch, sqlite3db1):
    assert_non_existing(monkeypatch, sqlite3db1, has_null_source=False)
