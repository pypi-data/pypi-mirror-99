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
from diffoscope.comparators.gzip import GzipFile
from diffoscope.comparators.binary import FilesystemFile
from diffoscope.comparators.missing_file import MissingFile
from diffoscope.comparators.utils.specialize import (
    specialize,
    is_direct_instance,
)

from ..utils.data import load_fixture, get_data
from ..utils.tools import skip_unless_file_version_is_at_least


gzip1 = load_fixture("test1.gz")
gzip2 = load_fixture("test2.gz")
gzip3 = load_fixture("debian-bug-876316-control.tar.gz")


def test_identification(gzip1):
    assert is_direct_instance(gzip1, GzipFile)


def test_fallback_recognizes(gzip3):
    # the below always-True assertion is just to document the fact that we
    # should identify it correctly regardless of any bugs in file(1)
    assert (
        "gzip" not in gzip3.magic_file_type or "gzip" in gzip3.magic_file_type
    )
    assert is_direct_instance(gzip3, GzipFile)


def test_no_differences(gzip1):
    difference = gzip1.compare(gzip1)
    assert difference is None


@pytest.fixture
def differences(gzip1, gzip2):
    return gzip1.compare(gzip2).details


@skip_unless_file_version_is_at_least("5.37")
def test_metadata(differences):
    assert differences[0].source1.startswith("filetype")
    assert differences[0].source2.startswith("filetype")
    expected_diff = get_data("gzip_metadata_expected_diff")
    assert differences[0].unified_diff == expected_diff


def test_content_source(differences):
    assert differences[1].source1 == "test1"
    assert differences[1].source2 == "test2"


def test_content_source_without_extension(tmpdir, gzip1, gzip2):
    path1 = str(tmpdir.join("test1"))
    path2 = str(tmpdir.join("test2"))
    shutil.copy(gzip1.path, path1)
    shutil.copy(gzip2.path, path2)
    gzip1 = specialize(FilesystemFile(path1))
    gzip2 = specialize(FilesystemFile(path2))
    difference = gzip1.compare(gzip2).details
    assert difference[1].source1 == "test1-content"
    assert difference[1].source2 == "test2-content"


def test_content_diff(differences):
    expected_diff = get_data("text_ascii_expected_diff")
    assert differences[1].unified_diff == expected_diff


def test_compare_non_existing(monkeypatch, gzip1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = gzip1.compare(MissingFile("/nonexisting", gzip1))
    assert difference.source2 == "/nonexisting"
    assert difference.details[-1].source2 == "/dev/null"
