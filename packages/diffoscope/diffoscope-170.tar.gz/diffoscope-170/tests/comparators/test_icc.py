#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2016 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016-2020 Chris Lamb <lamby@debian.org>
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
import subprocess

from diffoscope.config import Config
from diffoscope.comparators.icc import IccFile
from diffoscope.comparators.missing_file import MissingFile

from ..utils.data import load_fixture, get_data, data
from ..utils.tools import skip_unless_tools_exist, skip_unless_tool_is_at_least


icc1 = load_fixture("test1.icc")
icc2 = load_fixture("test2.icc")


def cd_iccdump_version():
    """
    The `cd-iccdump` command has no --version command and, whilst the `colord`
    binary does, it relies on the daemon running to return any output.
    Therefore we hackily compare the output (via the line length) of colord
    1.4.3:

        "  Profile ID    = 0477fa4bb5ae5ae9a778f5cd72eb45a4"

    ... versus, for example, colord 1.3.3:

        " Profile ID    = 0x0477fa4b"

    We don't massage the output (say, in an `Iccdump.filter` method) as it
    would remove the accuracy and, unfortunately, colord 1.4.3 also removes a
    somewhat-arbitrary newline too.
    """

    val = subprocess.check_output(("cd-iccdump", data("test1.icc"))).decode(
        "utf-8"
    )

    for x in val.splitlines():
        if x.startswith("  Profile ID") and len(x) == 47:
            return "1.4.3"
    return "1.3.3"


def test_identification(icc1):
    assert isinstance(icc1, IccFile)


def test_no_differences(icc1):
    difference = icc1.compare(icc1)
    assert difference is None


@pytest.fixture
def differences(icc1, icc2):
    return icc1.compare(icc2).details


@skip_unless_tool_is_at_least("cd-iccdump", cd_iccdump_version, "1.4.3")
def test_diff(differences):
    if "ne_SU" in differences[0].unified_diff:
        pytest.skip(
            "Endian-specific differences detected; see "
            "<https://bugs.debian.org/847595>"
        )

    expected_diff = get_data("icc_expected_diff")
    assert differences[0].unified_diff == expected_diff


@skip_unless_tools_exist("cd-iccdump")
def test_compare_non_existing(monkeypatch, icc1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = icc1.compare(MissingFile("/nonexisting", icc1))
    assert difference.source2 == "/nonexisting"
    assert len(difference.details) > 0
