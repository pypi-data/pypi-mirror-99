#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2015-2018, 2020 Chris Lamb <lamby@debian.org>
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
from diffoscope.comparators.java import ClassFile, ProcyonDecompiler, Javap
from diffoscope.comparators.missing_file import MissingFile

from ..utils.data import load_fixture, get_data
from ..utils.tools import (
    skip_unless_tools_exist,
    skip_unless_tool_is_at_least,
    skip_unless_tool_is_between,
)


class1 = load_fixture("Test1.class")
class2 = load_fixture("Test2.class")


def javap_version():
    try:
        out = subprocess.check_output(["javap", "-version"])
    except subprocess.CalledProcessError as e:
        out = e.output
    return out.decode("UTF-8").strip()


def test_identification(class1):
    assert isinstance(class1, ClassFile)


def test_no_differences(class1):
    difference = class1.compare(class1)
    assert difference is None


@pytest.fixture
def differences_procyon(monkeypatch, class1, class2):
    monkeypatch.setattr(class1, "decompilers", [ProcyonDecompiler])
    return class1.compare(class2).details


@pytest.fixture
def differences_javap(monkeypatch, class1, class2):
    monkeypatch.setattr(class1, "decompilers", [Javap])
    return class1.compare(class2).details


def diff(differences, expected_diff_file):
    expected_diff = get_data(expected_diff_file)
    assert differences[0].unified_diff == expected_diff


def compare_non_existing(monkeypatch, class1, decompiler):
    monkeypatch.setattr(Config(), "new_file", True)
    monkeypatch.setattr(class1, "decompilers", [decompiler])
    difference = class1.compare(MissingFile("/nonexisting", class1))
    assert difference.source2 == "/nonexisting"
    assert len(difference.details) > 0


@skip_unless_tools_exist("procyon")
def test_diff_procyon(differences_procyon):
    diff(differences_procyon, "procyon_class_expected_diff")


@skip_unless_tool_is_between("javap", javap_version, "9.0.4", "14.0")
def test_diff_javap(differences_javap):
    """
    Java tests are kept up to date relative to the JDK version bundled in
    Debian's `default-jdk` package. The output may vary depending on the JDK
    version installed on your system, rendering the tests inaccurate.
    """

    diff(differences_javap, "javap_class_expected_diff")


@skip_unless_tool_is_at_least("javap", javap_version, "14.0")
def test_diff_javap_14(differences_javap):
    diff(differences_javap, "javap_14_class_expected_diff")


@skip_unless_tools_exist("procyon")
def test_compare_non_existing_procyon(monkeypatch, class1):
    compare_non_existing(monkeypatch, class1, ProcyonDecompiler)


@skip_unless_tools_exist("javap")
def test_compare_non_existing_javap(monkeypatch, class1):
    compare_non_existing(monkeypatch, class1, Javap)
