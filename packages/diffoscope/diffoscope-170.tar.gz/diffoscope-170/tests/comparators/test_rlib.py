#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016 Ximin Luo <infinity0@debian.org>
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
from distutils.version import LooseVersion
from diffoscope.comparators.ar import ArFile

from ..utils import diff_ignore_line_numbers
from ..utils.data import load_fixture, get_data
from ..utils.tools import (
    skip_unless_tools_exist,
    skip_unless_tool_is_at_least,
    skip_if_binutils_does_not_support_x86,
)
from ..utils.nonexisting import assert_non_existing


rlib1 = load_fixture("test1.rlib")
rlib2 = load_fixture("test2.rlib")


@pytest.fixture(scope="function", autouse=True)
def init_tests(request, monkeypatch):
    # Make sure decompilation is disabled so that tests don't break
    monkeypatch.setattr(Config(), "exclude_commands", ["^radare2.*"])


def llvm_version():
    return (
        subprocess.check_output(["llvm-config", "--version"])
        .decode("utf-8")
        .strip()
    )


def test_identification(rlib1):
    assert isinstance(rlib1, ArFile)


def test_no_differences(rlib1):
    difference = rlib1.compare(rlib1)
    assert difference is None


@pytest.fixture
def differences(rlib1, rlib2):
    return rlib1.compare(rlib2).details


@pytest.fixture
def rlib_dis_expected_diff():
    actual_ver = llvm_version()

    if LooseVersion(str(actual_ver)) >= LooseVersion("3.8"):
        diff_file = "rlib_llvm_dis_expected_diff"

    if LooseVersion(str(actual_ver)) >= LooseVersion("5.0"):
        diff_file = "rlib_llvm_dis_expected_diff_5"

    if LooseVersion(str(actual_ver)) >= LooseVersion("7.0"):
        diff_file = "rlib_llvm_dis_expected_diff_7"

    if LooseVersion(str(actual_ver)) >= LooseVersion("10.0"):
        diff_file = "rlib_llvm_dis_expected_diff_10"

    return get_data(diff_file)


@skip_unless_tools_exist("nm")
def test_num_items(differences):
    assert len(differences) == 4


@skip_unless_tools_exist("nm")
@skip_if_binutils_does_not_support_x86()
def test_item0_armap(differences):
    assert differences[0].source1 == "nm -s {}"
    assert differences[0].source2 == "nm -s {}"
    expected_diff = get_data("rlib_armap_expected_diff")
    assert differences[0].unified_diff == expected_diff


@skip_unless_tools_exist("nm")
@skip_if_binutils_does_not_support_x86()
def test_item1_elf(differences):
    assert differences[1].source1 == "alloc_system-d16b8f0e.0.o"
    assert differences[1].source2 == "alloc_system-d16b8f0e.0.o"
    expected_diff = get_data("rlib_elf_expected_diff")
    assert differences[1].details[0].unified_diff == expected_diff


@skip_unless_tools_exist("nm")
def test_item2_rust_metadata_bin(differences):
    assert differences[2].source1 == "rust.metadata.bin"
    assert differences[2].source2 == "rust.metadata.bin"


@skip_unless_tools_exist("llvm-dis")
@skip_unless_tool_is_at_least("llvm-config", llvm_version, "3.8")
def test_item3_deflate_llvm_bitcode(differences, rlib_dis_expected_diff):
    assert differences[3].source1 == "alloc_system-d16b8f0e.0.bytecode.deflate"
    assert differences[3].source2 == "alloc_system-d16b8f0e.0.bytecode.deflate"
    expected_diff = rlib_dis_expected_diff
    actual_diff = differences[3].details[0].details[1].unified_diff
    assert diff_ignore_line_numbers(actual_diff) == diff_ignore_line_numbers(
        expected_diff
    )


@skip_unless_tools_exist("nm")
def test_compare_non_existing(monkeypatch, rlib1):
    assert_non_existing(monkeypatch, rlib1)
