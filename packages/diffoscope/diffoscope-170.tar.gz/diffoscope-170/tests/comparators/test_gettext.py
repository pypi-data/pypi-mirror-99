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

import codecs
import pytest

from diffoscope.config import Config
from diffoscope.comparators.missing_file import MissingFile
from diffoscope.comparators.gettext import MoFile

from ..utils.data import data, load_fixture, assert_diff
from ..utils.tools import skip_unless_tools_exist


mo1 = load_fixture("test1.mo")
mo2 = load_fixture("test2.mo")


def test_identification(mo1):
    assert isinstance(mo1, MoFile)


def test_no_differences(mo1):
    difference = mo1.compare(mo1)
    assert difference is None


@pytest.fixture
def differences(mo1, mo2):
    return mo1.compare(mo2).details


@skip_unless_tools_exist("msgunfmt")
def test_diff(differences):
    assert_diff(differences[0], "mo_expected_diff")


mo_no_charset = load_fixture("test_no_charset.mo")
mo_iso8859_1 = load_fixture("test_iso8859-1.mo")


@skip_unless_tools_exist("msgunfmt")
def test_charsets(mo_no_charset, mo_iso8859_1):
    difference = mo_no_charset.compare(mo_iso8859_1)
    expected_diff = codecs.open(
        data("mo_charsets_expected_diff"), encoding="utf-8"
    ).read()
    assert difference.details[0].unified_diff == expected_diff


@skip_unless_tools_exist("msgunfmt")
def test_compare_non_existing(monkeypatch, mo1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = mo1.compare(MissingFile("/nonexisting", mo1))
    assert difference.source2 == "/nonexisting"
    assert len(difference.details) > 0
