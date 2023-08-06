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

import pytest

import diffoscope.comparators

from diffoscope.config import Config
from diffoscope.comparators.deb import DebFile, Md5sumsFile, DebDataTarFile
from diffoscope.comparators.binary import FilesystemFile
from diffoscope.comparators.missing_file import MissingFile
from diffoscope.comparators.utils.specialize import specialize

from ..utils.tools import (
    skip_unless_tools_exist,
    skip_unless_file_version_is_at_least,
)
from ..utils.data import load_fixture, get_data


deb1 = load_fixture("test1.deb")
deb2 = load_fixture("test2.deb")


def test_identification(deb1):
    assert isinstance(deb1, DebFile)


def test_no_differences(deb1):
    difference = deb1.compare(deb1)
    assert difference is None


@pytest.fixture
def differences(deb1, deb2):
    return deb1.compare(deb2).details


def test_metadata(differences):
    expected_diff = get_data("deb_metadata_expected_diff")
    assert differences[0].unified_diff == expected_diff


def test_compressed_files(differences):
    assert differences[1].source1 == "control.tar.gz"
    assert differences[2].source1 == "data.tar.gz"


def test_identification_of_md5sums_outside_deb(tmpdir):
    path = str(tmpdir.join("md5sums"))
    open(path, "w")
    f = specialize(FilesystemFile(path))
    assert type(f) is FilesystemFile


def test_identification_of_md5sums_in_deb(deb1, deb2, monkeypatch):
    orig_func = Md5sumsFile.recognizes

    @staticmethod
    def probe(file):
        ret = orig_func(file)
        if ret:
            test_identification_of_md5sums_in_deb.found = True
        return ret

    test_identification_of_md5sums_in_deb.found = False
    monkeypatch.setattr(Md5sumsFile, "recognizes", probe)
    deb1.compare(deb2)
    assert test_identification_of_md5sums_in_deb.found


def test_md5sums(differences):
    assert differences[1].details[0].details[1].details[0].comment
    # we skip diffing the md5sums since it's not interesting, the actual files are diffed instead
    assert not differences[1].details[0].details[1].details[0].unified_diff
    assert not differences[1].details[0].details[1].details[0].details


def test_identical_files_in_md5sums(deb1, deb2):
    for name in [
        "./usr/share/doc/test/README.Debian",
        "./usr/share/doc/test/copyright",
    ]:
        assert deb1.md5sums[name] == deb2.md5sums[name]


def test_identification_of_data_tar(deb1, deb2, monkeypatch):
    orig_func = DebDataTarFile.recognizes

    @staticmethod
    def probe(file):
        ret = orig_func(file)
        if ret:
            test_identification_of_data_tar.found = True
        return ret

    test_identification_of_data_tar.found = False
    monkeypatch.setattr(DebDataTarFile, "recognizes", probe)
    deb1.compare(deb2)
    assert test_identification_of_data_tar.found


def test_skip_comparison_of_known_identical_files(deb1, deb2, monkeypatch):
    compared = set()
    orig_func = diffoscope.comparators.utils.compare.compare_files

    def probe(file1, file2, **kwargs):
        compared.add(file1.name)
        return orig_func(file1, file2, **kwargs)

    monkeypatch.setattr(
        diffoscope.comparators.utils.compare, "compare_files", probe
    )
    deb1.compare(deb2)
    assert "./usr/share/doc/test/README.Debian" not in compared


def test_compare_non_existing(monkeypatch, deb1):
    monkeypatch.setattr(Config(), "new_file", True)
    difference = deb1.compare(MissingFile("/nonexisting", deb1))
    assert difference.source2 == "/nonexisting"
    assert difference.details[-1].source2 == "/dev/null"


bug881937_deb1 = load_fixture("bug881937_1.deb")
bug881937_deb2 = load_fixture("bug881937_2.deb")
bug903391_deb1 = load_fixture("bug903391_1.deb")
bug903391_deb2 = load_fixture("bug903391_2.deb")
bug903401_deb1 = load_fixture("bug903401_1.deb")
bug903401_deb2 = load_fixture("bug903401_2.deb")
bug903565_deb1 = load_fixture("bug903565_1.deb")
bug903565_deb2 = load_fixture("bug903565_2.deb")


@skip_unless_tools_exist("xz")
@skip_unless_file_version_is_at_least("5.37")
def test_compare_different_compression(bug881937_deb1, bug881937_deb2):
    difference = bug881937_deb1.compare(bug881937_deb2)
    assert difference.details[2].source1 == "control.tar.gz"
    assert difference.details[2].source2 == "control.tar.xz"
    expected_diff = get_data("bug881937_control_expected_diff")
    assert (
        difference.details[2].details[2].details[1].unified_diff
        == expected_diff
    )


def test_uncompressed_data_tar(bug903401_deb1, bug903401_deb2):
    bug903401_deb1.compare(bug903401_deb2)


def test_uncompressed_control_tar(bug903391_deb1, bug903391_deb2):
    bug903391_deb1.compare(bug903391_deb2)


def test_compare_different_compression_multiple_files(
    bug903565_deb1, bug903565_deb2
):
    bug903565_deb1.compare(bug903565_deb2)
