#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
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
from diffoscope.comparators.fonts import TtfFile
from diffoscope.comparators.missing_file import MissingFile

from ..utils.data import load_fixture, assert_diff
from ..utils.tools import skip_unless_tools_exist


ttf1 = load_fixture("Samyak-Malayalam1.ttf")
ttf2 = load_fixture("Samyak-Malayalam2.ttf")


def test_identification(ttf1):
    assert isinstance(ttf1, TtfFile)


def test_no_differences(ttf1):
    difference = ttf1.compare(ttf1)
    assert difference is None


@pytest.fixture
def differences(ttf1, ttf2):
    return ttf1.compare(ttf2).details


@skip_unless_tools_exist("showttf")
def test_diff(differences):
    assert_diff(differences[0], "ttf_expected_diff")


@skip_unless_tools_exist("showttf")
def test_compare_non_existing(monkeypatch, ttf1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = ttf1.compare(MissingFile("/nonexisting", ttf1))
    assert difference.source2 == "/nonexisting"
    assert len(difference.details) > 0
