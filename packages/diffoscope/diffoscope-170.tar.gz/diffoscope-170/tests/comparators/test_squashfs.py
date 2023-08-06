#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2015-2017, 2019-2020 Chris Lamb <lamby@debian.org>
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

from diffoscope.comparators.squashfs import SquashfsFile

from ..utils.data import load_fixture, get_data
from ..utils.tools import skip_unless_tools_exist, skip_unless_tool_is_at_least
from ..utils.nonexisting import assert_non_existing


def unsquashfs_version():
    # first line of 'unsquashfs -version' looks like:
    #   unsquashfs version 4.4pre-git (2019/08/15)
    try:
        out = subprocess.check_output(["unsquashfs", "-version"])
    except subprocess.CalledProcessError as e:
        out = e.output
    return out.decode("UTF-8").splitlines()[0].split()[2].strip()


squashfs1 = load_fixture("test1.squashfs")
squashfs2 = load_fixture("test2.squashfs")


def test_identification(squashfs1):
    assert isinstance(squashfs1, SquashfsFile)


def test_no_differences(squashfs1):
    difference = squashfs1.compare(squashfs1)
    assert difference is None


def test_no_warnings(capfd, squashfs1, squashfs2):
    _ = squashfs1.compare(squashfs2)
    _, err = capfd.readouterr()
    assert err == ""


@pytest.fixture
def differences(squashfs1, squashfs2):
    return squashfs1.compare(squashfs2).details


@skip_unless_tool_is_at_least("unsquashfs", unsquashfs_version, "4.4")
def test_superblock(differences):
    expected_diff = get_data("squashfs_superblock_expected_diff")
    assert differences[0].unified_diff == expected_diff


@skip_unless_tools_exist("unsquashfs")
def test_symlink(differences):
    assert differences[2].comment == "symlink"
    expected_diff = get_data("symlink_expected_diff")
    assert differences[2].unified_diff == expected_diff


@skip_unless_tools_exist("unsquashfs")
def test_compressed_files(differences):
    assert differences[3].source1 == "/text"
    assert differences[3].source2 == "/text"
    expected_diff = get_data("text_ascii_expected_diff")
    assert differences[3].unified_diff == expected_diff


@skip_unless_tools_exist("unsquashfs")
def test_compare_non_existing(monkeypatch, squashfs1):
    assert_non_existing(monkeypatch, squashfs1)
