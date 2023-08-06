#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Daniel Kahn Gillmor <dkg@fifthhorseman.net>
# Copyright © 2015 Paul Gevers <elbrus@debian.org>
# Copyright © 2016-2018, 2020 Chris Lamb <lamby@debian.org>
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

from diffoscope.comparators.ppu import PpuFile

from ..utils.data import load_fixture, assert_diff
from ..utils.tools import skip_unless_tools_exist, skip_unless_tool_is_at_least
from ..utils.nonexisting import assert_non_existing


# These test files were taken from two different builds of the Debian package
# fp-units-castle-game-engine (version 5.1.1-2 on amd64) on the Debian
# reproducible build infrastructure. The files were originally called
# castletexturefont_dejavusans_10.ppu which are generated during package
# building of the cge package from dejavusans font in the fonts-dejavu package.

file1 = load_fixture("test1.ppu")
file2 = load_fixture("test2.ppu")


def ppudump_version():
    # first line of `PPU-Analyser Version 3.0.0` looks like:
    #   PPU-Analyser Version 3.0.0
    out = subprocess.check_output(["ppudump", "-h"])
    return out.decode("utf-8").splitlines()[0].split()[2].strip()


@skip_unless_tool_is_at_least("ppudump", ppudump_version, "3.2.0")
def test_identification(file1):
    assert isinstance(file1, PpuFile)


def test_no_differences(file1):
    assert file1.compare(file1) is None


@pytest.fixture
def differences(file1, file2):
    return file1.compare(file2).details


@skip_unless_tool_is_at_least("ppudump", ppudump_version, "3.2.0")
def test_diff(differences):
    assert_diff(differences[0], "ppu_expected_diff")


@skip_unless_tool_is_at_least("ppudump", ppudump_version, "3.2.0")
def test_compare_non_existing(monkeypatch, file1):
    assert_non_existing(monkeypatch, file1, has_null_source=False)
