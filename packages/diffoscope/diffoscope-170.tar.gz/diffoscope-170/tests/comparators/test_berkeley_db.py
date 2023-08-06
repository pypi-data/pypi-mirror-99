#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2018, 2020 Chris Lamb <lamby@debian.org>
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

from diffoscope.comparators.berkeley_db import BerkeleyDBFile

from ..utils.data import load_fixture, assert_diff
from ..utils.tools import skip_unless_tools_exist
from ..utils.nonexisting import assert_non_existing

db1 = load_fixture("test1.db")
db2 = load_fixture("test2.db")


def test_identification(db1):
    assert isinstance(db1, BerkeleyDBFile)


@pytest.fixture
def differences(db1, db2):
    return db1.compare(db2).details


def test_no_differences(db1):
    difference = db1.compare(db1)
    assert difference is None


@skip_unless_tools_exist("db_dump")
def test_diff(differences):
    assert_diff(differences[0], "berkeley_db_expected_diff")


@skip_unless_tools_exist("db_dump")
def test_compare_non_existing(monkeypatch, db1):
    assert_non_existing(monkeypatch, db1, has_null_source=False)
