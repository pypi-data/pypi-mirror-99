#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016-2017, 2019-2020 Chris Lamb <lamby@debian.org>
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

import struct
import pytest
import re
import subprocess

from diffoscope.comparators.cbfs import CbfsFile
from diffoscope.comparators.binary import FilesystemFile
from diffoscope.comparators.utils.specialize import specialize

from ..utils.data import data, get_data
from ..utils.tools import skip_unless_tools_exist
from ..utils.nonexisting import assert_non_existing


TEST_FILE1_PATH = data("text_ascii1")
TEST_FILE2_PATH = data("text_ascii2")


@pytest.fixture
def rom1(tmpdir):
    path = str(tmpdir.join("coreboot1"))

    subprocess.check_call(
        ("cbfstool", path, "create", "-m", "x86", "-s", "32768")
    )

    subprocess.check_call(
        (
            "cbfstool",
            path,
            "add",
            "-f",
            TEST_FILE1_PATH,
            "-n",
            "text",
            "-t",
            "raw",
        ),
    )

    return specialize(FilesystemFile(path))


@pytest.fixture
def rom2(tmpdir):
    size = 32768
    path = str(tmpdir.join("coreboot2.rom"))

    subprocess.check_call(
        ("cbfstool", path, "create", "-m", "x86", "-s", "%s" % size),
    )

    subprocess.check_call(
        (
            "cbfstool",
            path,
            "add",
            "-f",
            TEST_FILE2_PATH,
            "-n",
            "text",
            "-t",
            "raw",
        ),
        shell=False,
    )

    # Remove the last 4 bytes to exercise the full header search
    buf = bytearray(size)
    with open(path, "rb") as f:
        f.readinto(buf)

    with open(path, "wb") as f:
        size = struct.unpack_from("!I", buf, offset=len(buf) - 4 - 32 + 8)[0]
        struct.pack_into("!I", buf, len(buf) - 4 - 32 + 8, size - 4)
        f.write(buf[:-4])

    return specialize(FilesystemFile(path))


@skip_unless_tools_exist("cbfstool")
def test_identification_using_offset(rom1):
    assert isinstance(rom1, CbfsFile)


@skip_unless_tools_exist("cbfstool")
def test_identification_without_offset(rom2):
    assert isinstance(rom2, CbfsFile)


@skip_unless_tools_exist("cbfstool")
def test_no_differences(rom1):
    difference = rom1.compare(rom1)
    assert difference is None


@pytest.fixture
def differences(rom1, rom2):
    difference = rom1.compare(rom2)
    return difference.details


@skip_unless_tools_exist("cbfstool")
def test_listing(differences):
    # Compares outputs of: "cbfstool $tmpdir/coreboot*.rom print"
    #
    # As the output of this command keeps changing slightly (see
    # https://salsa.debian.org/reproducible-builds/diffoscope/merge_requests/38/
    # and the git log of this file), perform only these basic coherence check.

    assert differences[0].source1.startswith("cbfstool")
    assert re.search(r"\+text\s.*\sraw\s", differences[0].unified_diff)


@skip_unless_tools_exist("cbfstool")
def test_content(differences):
    assert differences[1].source1 == "text"
    assert differences[1].source2 == "text"
    expected_diff = get_data("text_ascii_expected_diff")
    assert differences[1].unified_diff == expected_diff


@skip_unless_tools_exist("cbfstool")
def test_compare_non_existing(monkeypatch, rom1):
    assert_non_existing(monkeypatch, rom1)
