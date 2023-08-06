#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Daniel Kahn Gillmor <dkg@fifthhorseman.net>
# Copyright © 2015-2017, 2020 Chris Lamb <lamby@debian.org>
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

from diffoscope.config import Config
from diffoscope.comparators.mono import MonoExeFile
from diffoscope.comparators.missing_file import MissingFile

from ..utils.data import load_fixture, get_data
from ..utils.tools import skip_unless_tools_exist


# these were generated with:

# echo 'public class Test { static public void Main () {} }' > test.cs
# mcs -out:test1.exe test.cs ; sleep 2; mcs -out:test2.exe test.cs

exe1 = load_fixture("test1.exe")
exe2 = load_fixture("test2.exe")


def test_identification(exe1):
    assert isinstance(exe1, MonoExeFile)


def test_no_differences(exe1):
    difference = exe1.compare(exe1)
    assert difference is None


@pytest.fixture
def differences(exe1, exe2):
    return exe1.compare(exe2).details


@skip_unless_tools_exist("pedump")
def test_diff(differences):
    expected_diff = get_data("pe_expected_diff")
    assert differences[0].unified_diff == expected_diff


@skip_unless_tools_exist("pedump")
def test_compare_non_existing(monkeypatch, exe1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = exe1.compare(MissingFile("/nonexisting", exe1))
    assert difference.source2 == "/nonexisting"
    assert len(difference.details) > 0
