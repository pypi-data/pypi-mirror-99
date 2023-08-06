#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2017 Maria Glukhova <siammezzze@gmail.com>
# Copyright © 2017, 2019-2021 Chris Lamb <lamby@debian.org>
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

import sys
import pytest
import subprocess

from diffoscope.comparators.apk import ApkFile

from ..utils.data import load_fixture, assert_diff
from ..utils.tools import skip_unless_tools_exist, skip_unless_tool_is_at_least
from ..utils.nonexisting import assert_non_existing

apk1 = load_fixture("test1.apk")
apk2 = load_fixture("test2.apk")
apk3 = load_fixture("test3.apk")


def apktool_version():
    return (
        subprocess.check_output(["apktool", "-version"])
        .decode("utf-8")
        .strip()
    )


def test_identification(apk1):
    assert isinstance(apk1, ApkFile)


def test_no_differences(apk1):
    difference = apk1.compare(apk1)
    assert difference is None


@pytest.fixture
def differences(apk1, apk2):
    return apk1.compare(apk2).details


@pytest.fixture
def differences2(apk1, apk3):
    return apk1.compare(apk3).details


@skip_unless_tools_exist("apktool", "zipinfo")
def test_compare_non_existing(monkeypatch, apk1):
    assert_non_existing(monkeypatch, apk1)


@skip_unless_tools_exist("apktool", "zipinfo")
def test_zipinfo(differences):
    assert differences[0].source1 == "zipinfo {}"
    assert differences[0].source2 == "zipinfo {}"
    assert_diff(differences[0], "apk_zipinfo_expected_diff")


@pytest.mark.xfail(strict=False)
@skip_unless_tools_exist("zipinfo")
@skip_unless_tool_is_at_least("apktool", apktool_version, "2.5.0")
@pytest.mark.skipif(
    sys.version_info < (3, 8), reason="requires Python 3.8 or higher"
)
def test_android_manifest(differences):
    assert differences[1].source1 == "AndroidManifest.xml (decoded)"
    assert differences[1].source2 == "AndroidManifest.xml (decoded)"
    assert_diff(differences[1].details[0], "apk_manifest_expected_diff")


@skip_unless_tools_exist("apktool", "zipinfo")
def test_apk_metadata_source(differences):
    assert differences[2].source1 == "APK metadata"
    assert differences[2].source2 == "APK metadata"


@skip_unless_tools_exist("apktool", "zipinfo")
def test_skip_undecoded_android_manifest(differences):
    assert not any(
        difference.source1 == "original/AndroidManifest.xml"
        for difference in differences
    )
    assert not any(
        difference.source2 == "original/AndroidManifest.xml"
        for difference in differences
    )
    undecoded_manifest = "AndroidManifest.xml (original / undecoded)"
    assert not any(
        difference.source1 == undecoded_manifest for difference in differences
    )
    assert not any(
        difference.source2 == undecoded_manifest for difference in differences
    )


@skip_unless_tools_exist("apktool", "zipinfo")
def test_no_android_manifest(differences2):
    undecoded_manifest = "AndroidManifest.xml (original / undecoded)"
    assert differences2[2].source1 == undecoded_manifest
    assert differences2[2].source2 == undecoded_manifest
    assert (
        differences2[2].comment == "No decoded AndroidManifest.xml "
        "found for one of the APK files."
    )
