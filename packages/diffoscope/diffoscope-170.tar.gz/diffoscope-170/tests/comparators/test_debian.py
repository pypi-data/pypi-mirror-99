#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
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

import shutil
import pytest

from diffoscope.config import Config
from diffoscope.comparators import ComparatorManager
from diffoscope.comparators.binary import FilesystemFile
from diffoscope.comparators.missing_file import MissingFile
from diffoscope.comparators.utils.specialize import specialize

from ..utils.data import data, get_data
from ..utils.tools import skip_unless_module_exists

from ..utils.nonexisting import assert_non_existing

try:
    from diffoscope.comparators.debian import (
        DotChangesFile,
        DotDscFile,
        DotBuildinfoFile,
    )
except ImportError:
    from diffoscope.comparators.debian_fallback import (
        DotChangesFile,
        DotDscFile,
        DotBuildinfoFile,
    )

TEST_DOT_CHANGES_FILE1_PATH = data("test1.changes")
TEST_DOT_CHANGES_FILE2_PATH = data("test2.changes")
TEST_DOT_CHANGES_FILE3_PATH = data("test3.changes")
TEST_DOT_CHANGES_FILE4_PATH = data("test4.changes")
TEST_DOT_BUILDINFO_FILE1_PATH = data("test1.buildinfo")
TEST_DOT_BUILDINFO_FILE2_PATH = data("test2.buildinfo")
TEST_DEB_FILE1_PATH = data("test1.deb")
TEST_DEB_FILE2_PATH = data("test2.deb")


@pytest.fixture
def dot_changes1(tmpdir):
    tmpdir.mkdir("a")
    dot_changes_path = str(tmpdir.join("a/test_1.changes"))
    shutil.copy(TEST_DOT_CHANGES_FILE1_PATH, dot_changes_path)
    shutil.copy(TEST_DEB_FILE1_PATH, str(tmpdir.join("a/test_1_all.deb")))
    shutil.copy(
        TEST_DOT_BUILDINFO_FILE1_PATH, str(tmpdir.join("a/test_1.buildinfo"))
    )
    return specialize(FilesystemFile(dot_changes_path))


@pytest.fixture
def dot_changes2(tmpdir):
    tmpdir.mkdir("b")
    dot_changes_path = str(tmpdir.join("b/test_1.changes"))
    shutil.copy(TEST_DOT_CHANGES_FILE2_PATH, dot_changes_path)
    shutil.copy(TEST_DEB_FILE2_PATH, str(tmpdir.join("b/test_1_all.deb")))
    shutil.copy(
        TEST_DOT_BUILDINFO_FILE2_PATH, str(tmpdir.join("b/test_2.buildinfo"))
    )
    return specialize(FilesystemFile(dot_changes_path))


@pytest.fixture
def dot_changes3(tmpdir):
    tmpdir.mkdir("c")
    dot_changes_path = str(tmpdir.join("c/test_3.changes"))
    shutil.copy(TEST_DOT_CHANGES_FILE3_PATH, dot_changes_path)
    shutil.copy(TEST_DEB_FILE1_PATH, str(tmpdir.join("c/test_1_all.deb")))
    shutil.copy(
        TEST_DOT_BUILDINFO_FILE2_PATH, str(tmpdir.join("c/test_2.buildinfo"))
    )
    return specialize(FilesystemFile(dot_changes_path))


@pytest.fixture
def dot_changes4(tmpdir):
    tmpdir.mkdir("d")
    dot_changes_path = str(tmpdir.join("d/test_4.changes"))
    shutil.copy(TEST_DOT_CHANGES_FILE4_PATH, dot_changes_path)
    shutil.copy(TEST_DEB_FILE2_PATH, str(tmpdir.join("d/test_1_all.deb")))
    shutil.copy(
        TEST_DOT_BUILDINFO_FILE1_PATH, str(tmpdir.join("d/test_2.buildinfo"))
    )
    return specialize(FilesystemFile(dot_changes_path))


def test_dot_changes_identification(dot_changes1):
    assert isinstance(dot_changes1, DotChangesFile)


@skip_unless_module_exists("debian.deb822")
def test_dot_changes_invalid(tmpdir):
    tmpdir.mkdir("a")
    dot_changes_path = str(tmpdir.join("a/test_1.changes"))
    shutil.copy(TEST_DOT_CHANGES_FILE1_PATH, dot_changes_path)
    # we don't copy the referenced .deb
    identified = specialize(FilesystemFile(dot_changes_path))
    assert not isinstance(identified, DotChangesFile)


def test_dot_changes_no_differences(dot_changes1):
    difference = dot_changes1.compare(dot_changes1)
    assert difference is None


@pytest.fixture
def dot_changes_differences(dot_changes1, dot_changes2):
    difference = dot_changes1.compare(dot_changes2)
    assert difference.source2 == "/nonexisting"
    assert difference.details[-1].source2 == "/dev/null"


@pytest.fixture
def dot_changes_differences_identical_contents_and_identical_files(
    dot_changes1, dot_changes3
):
    difference = dot_changes1.compare(dot_changes3)
    return difference.details


@pytest.fixture
def dot_changes_differences_identical_contents_and_different_files(
    dot_changes1, dot_changes4
):
    difference = dot_changes1.compare(dot_changes4)
    return difference.details


@pytest.fixture
def dot_changes_differences_different_contents_and_identical_files(
    dot_changes2, dot_changes4
):
    difference = dot_changes4.compare(dot_changes2)
    return difference.details


@skip_unless_module_exists("debian.deb822")
def test_dot_changes_no_differences_exclude_buildinfo(
    dot_changes1, dot_changes3
):
    difference = dot_changes1.compare(dot_changes3)
    assert difference is None


@skip_unless_module_exists("debian.deb822")
def test_dot_changes_identical_contents_and_different_files(
    dot_changes_differences_identical_contents_and_different_files,
):
    assert dot_changes_differences_identical_contents_and_different_files[0]
    expected_diff = get_data(
        "dot_changes_identical_contents_and_different_files_expected_diff"
    )
    assert (
        dot_changes_differences_identical_contents_and_different_files[
            0
        ].unified_diff
        == expected_diff
    )


@skip_unless_module_exists("debian.deb822")
def test_dot_changes_different_contents_and_identical_files(
    dot_changes_differences_different_contents_and_identical_files,
):
    assert dot_changes_differences_different_contents_and_identical_files[0]
    assert dot_changes_differences_different_contents_and_identical_files[1]
    expected_diff_contents = get_data("dot_changes_description_expected_diff")
    expected_diff_files = get_data(
        "dot_changes_different_contents_and_identical_files_expected_diff"
    )
    assert (
        dot_changes_differences_different_contents_and_identical_files[
            0
        ].unified_diff
        == expected_diff_contents
    )
    assert (
        dot_changes_differences_different_contents_and_identical_files[
            1
        ].unified_diff
        == expected_diff_files
    )


TEST_DOT_DSC_FILE1_PATH = data("test1.dsc")
TEST_DOT_DSC_FILE2_PATH = data("test2.dsc")
TEST_DEB_SRC1_PATH = data("test1.debsrc.tar.gz")
TEST_DEB_SRC2_PATH = data("test2.debsrc.tar.gz")


@pytest.fixture
def dot_dsc1(tmpdir):
    tmpdir.mkdir("a")
    dot_dsc_path = str(tmpdir.join("a/test_1.dsc"))
    shutil.copy(TEST_DOT_DSC_FILE1_PATH, dot_dsc_path)
    shutil.copy(TEST_DEB_SRC1_PATH, str(tmpdir.join("a/test_1.tar.gz")))
    return specialize(FilesystemFile(dot_dsc_path))


@pytest.fixture
def dot_dsc2(tmpdir):
    tmpdir.mkdir("b")
    dot_dsc_path = str(tmpdir.join("b/test_1.dsc"))
    shutil.copy(TEST_DOT_DSC_FILE2_PATH, dot_dsc_path)
    shutil.copy(TEST_DEB_SRC2_PATH, str(tmpdir.join("b/test_1.tar.gz")))
    return specialize(FilesystemFile(dot_dsc_path))


def test_dot_dsc_identification(dot_dsc1):
    assert isinstance(dot_dsc1, DotDscFile)


@skip_unless_module_exists("debian.deb822")
def test_dot_dsc_no_associated_tar_gz(tmpdir, dot_dsc2):
    tmpdir.mkdir("a")
    dot_dsc_path = str(tmpdir.join("a/test_1.dsc"))
    shutil.copy(TEST_DOT_CHANGES_FILE1_PATH, dot_dsc_path)
    # we don't copy the referenced .tar.gz
    identified = specialize(FilesystemFile(dot_dsc_path))
    assert isinstance(identified, DotDscFile)


def test_dot_dsc_no_differences(dot_dsc1):
    difference = dot_dsc1.compare(dot_dsc1)
    assert difference is None


@pytest.fixture
def dot_dsc_differences(dot_dsc1, dot_dsc2):
    difference = dot_dsc1.compare(dot_dsc2)
    return difference.details


@skip_unless_module_exists("debian.deb822")
def test_dot_dsc_internal_diff(dot_dsc_differences):
    assert dot_dsc_differences[1].source1 == "test_1.tar.gz"


@skip_unless_module_exists("debian.deb822")
def test_dot_dsc_compare_non_existing(monkeypatch, dot_dsc1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = dot_dsc1.compare(MissingFile("/nonexisting", dot_dsc1))
    assert difference.source2 == "/nonexisting"
    assert difference.details[-1].source2 == "/dev/null"


@pytest.fixture
def dot_buildinfo1(tmpdir):
    tmpdir.mkdir("a")
    dot_buildinfo_path = str(tmpdir.join("a/test_1.buildinfo"))
    shutil.copy(TEST_DOT_BUILDINFO_FILE1_PATH, dot_buildinfo_path)
    shutil.copy(TEST_DOT_DSC_FILE1_PATH, str(tmpdir.join("a/test_1.dsc")))
    shutil.copy(TEST_DEB_FILE1_PATH, str(tmpdir.join("a/test_1_all.deb")))
    return specialize(FilesystemFile(dot_buildinfo_path))


@pytest.fixture
def dot_buildinfo2(tmpdir):
    tmpdir.mkdir("b")
    dot_buildinfo_path = str(tmpdir.join("b/test_1.buildinfo"))
    shutil.copy(TEST_DOT_BUILDINFO_FILE2_PATH, dot_buildinfo_path)
    shutil.copy(TEST_DOT_DSC_FILE2_PATH, str(tmpdir.join("b/test_1.dsc")))
    shutil.copy(TEST_DEB_FILE2_PATH, str(tmpdir.join("b/test_1_all.deb")))
    return specialize(FilesystemFile(dot_buildinfo_path))


def test_dot_buildinfo_identification(dot_buildinfo1):
    assert isinstance(dot_buildinfo1, DotBuildinfoFile)


@skip_unless_module_exists("debian.deb822")
def test_dot_buildinfo_no_deb(tmpdir):
    tmpdir.mkdir("a")
    dot_buildinfo_path = str(tmpdir.join("a/test_1.buildinfo"))
    shutil.copy(TEST_DOT_BUILDINFO_FILE1_PATH, dot_buildinfo_path)
    # we don't copy the referenced .deb
    identified = specialize(FilesystemFile(dot_buildinfo_path))
    assert isinstance(identified, DotBuildinfoFile)


def test_dot_buildinfo_no_differences(dot_buildinfo1):
    difference = dot_buildinfo1.compare(dot_buildinfo1)
    assert difference is None


@pytest.fixture
def dot_buildinfo_differences(dot_buildinfo1, dot_buildinfo2):
    difference = dot_buildinfo1.compare(dot_buildinfo2)
    return difference.details


@skip_unless_module_exists("debian.deb822")
def test_dot_buildinfo_internal_diff(dot_buildinfo_differences):
    assert dot_buildinfo_differences[1].source1 == "test_1_all.deb"


@skip_unless_module_exists("debian.deb822")
def test_dot_buildinfo_compare_non_existing(monkeypatch, dot_buildinfo1):
    assert_non_existing(monkeypatch, dot_buildinfo1)


def test_fallback_comparisons(monkeypatch):
    manager = ComparatorManager()
    monkeypatch.setattr(
        manager,
        "COMPARATORS",
        (
            ("debian_fallback.DotChangesFile",),
            ("debian_fallback.DotDscFile",),
            ("debian_fallback.DotBuildinfoFile",),
        ),
    )
    manager.reload()

    for a, b, expected_diff in (
        (
            "test1.changes",
            "test2.changes",
            "dot_changes_fallback_expected_diff",
        ),
        ("test1.dsc", "test2.dsc", "dot_dsc_fallback_expected_diff"),
        (
            "test1.buildinfo",
            "test2.buildinfo",
            "dot_buildinfo_fallback_expected_diff",
        ),
    ):
        # Re-specialize after reloading our Comparators
        file1 = specialize(FilesystemFile(data(a)))
        file2 = specialize(FilesystemFile(data(b)))

        assert file1.compare(file1) is None
        assert file2.compare(file2) is None
        assert file1.compare(file2).unified_diff == get_data(expected_diff)
