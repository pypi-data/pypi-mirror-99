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

import os.path
import pytest
import subprocess

from os import mkdir, symlink
from tempfile import TemporaryDirectory

from diffoscope.tools import tool_required
from diffoscope.exc import RequiredToolNotFound
from diffoscope.difference import Difference
from diffoscope.comparators.binary import FilesystemFile
from diffoscope.comparators.utils.file import File
from diffoscope.comparators.missing_file import MissingFile
from diffoscope.comparators.utils.compare import Xxd

from ..utils.data import data, init_fixture, get_data, normalize_zeros
from ..utils.tools import skip_unless_tools_exist, skip_unless_module_exists


TEST_FILE1_PATH = data("binary1")
TEST_FILE2_PATH = data("binary2")
TEST_ASCII_PATH = data("text_ascii1")
TEST_UNICODE_PATH = data("text_unicode1")
TEST_ISO8859_PATH = data("text_iso8859")


binary1 = init_fixture(TEST_FILE1_PATH)
binary2 = init_fixture(TEST_FILE2_PATH)


def test_same_content(binary1):
    assert binary1.has_same_content_as(binary1) is True


def test_not_same_content(binary1, binary2):
    assert binary1.has_same_content_as(binary2) is False


def test_guess_file_type():
    assert File.guess_file_type(TEST_FILE1_PATH) == "data"


def test_guess_encoding_binary():
    assert File.guess_encoding(TEST_FILE1_PATH) == "binary"


def test_guess_encoding_ascii():
    assert File.guess_encoding(TEST_ASCII_PATH) == "us-ascii"


def test_guess_encoding_unicode():
    assert File.guess_encoding(TEST_UNICODE_PATH) == "utf-8"


def test_guess_encoding_iso8859():
    assert File.guess_encoding(TEST_ISO8859_PATH) == "iso-8859-1"


def test_no_differences_with_xxd(binary1):
    difference = binary1.compare_bytes(binary1)
    assert difference is None


@skip_unless_tools_exist("xxd")
def test_compare_with_xxd(binary1, binary2):
    difference = binary1.compare_bytes(binary2)
    expected_diff = get_data("binary_expected_diff")
    assert normalize_zeros(difference.unified_diff) == expected_diff


def test_compare_non_existing_with_xxd(binary1):
    difference = binary1.compare_bytes(MissingFile("/nonexisting", binary1))
    assert difference.source2 == "/nonexisting"


@pytest.fixture
def xxd_not_found(monkeypatch):
    def mock_cmdline(self):
        raise RequiredToolNotFound("xxd")

    monkeypatch.setattr(Xxd, "cmdline", mock_cmdline)


def test_no_differences_without_xxd(xxd_not_found, binary1):
    difference = binary1.compare_bytes(binary1)
    assert difference is None


def test_compare_without_xxd(xxd_not_found, binary1, binary2):
    difference = binary1.compare(binary2)
    expected_diff = get_data("binary_hexdump_expected_diff")
    assert difference.unified_diff == expected_diff


def test_with_compare_details():
    d = Difference("diff", TEST_FILE1_PATH, TEST_FILE2_PATH, source="source")

    class MockFile(FilesystemFile):
        def compare_details(self, other, source=None):
            return [d]

    difference = MockFile(TEST_FILE1_PATH).compare(
        MockFile(TEST_FILE2_PATH), source="source"
    )
    assert difference.details[0] == d


@skip_unless_tools_exist("xxd")
def test_with_compare_details_and_fallback():
    class MockFile(FilesystemFile):
        DESCRIPTION = "mock files"

        def compare_details(self, other, source=None):
            return []

    difference = MockFile(TEST_FILE1_PATH).compare(MockFile(TEST_FILE2_PATH))
    expected_diff = get_data("binary_expected_diff")
    assert (
        "supported for mock files but no file-specific differences were detected"
        in difference.comment
    )
    assert normalize_zeros(difference.unified_diff) == expected_diff


def test_with_compare_details_and_no_actual_differences():
    class MockFile(FilesystemFile):
        def compare_details(self, other, source=None):
            return []

    difference = MockFile(TEST_FILE1_PATH).compare(MockFile(TEST_FILE1_PATH))
    assert difference is None


@skip_unless_tools_exist("xxd")
def test_with_compare_details_and_failed_process():
    output = "Free Jeremy Hammond"

    class MockFile(FilesystemFile):
        def compare_details(self, other, source=None):
            subprocess.check_call(["sh", "-c", 'echo "%s"; exit 42' % output])
            raise Exception("should not be run")

    difference = MockFile(TEST_FILE1_PATH).compare(MockFile(TEST_FILE2_PATH))
    expected_diff = get_data("../data/binary_expected_diff")
    assert output in difference.comment
    assert "42" in difference.comment
    assert normalize_zeros(difference.unified_diff) == expected_diff


@skip_unless_tools_exist("xxd")
def test_with_compare_details_and_parsing_error():
    from diffoscope.exc import OutputParsingError

    class MockFile(FilesystemFile):
        def compare_details(self, other, source=None):
            subprocess.check_output(["sh", "-c", "exit 0"])
            raise OutputParsingError("sh", self)

    difference = MockFile(TEST_FILE1_PATH).compare(MockFile(TEST_FILE2_PATH))
    expected_diff = get_data("../data/binary_expected_diff")
    assert "Error parsing output" in difference.comment
    assert normalize_zeros(difference.unified_diff) == expected_diff


@skip_unless_tools_exist("xxd")
def test_with_compare_details_and_extraction_error():
    from diffoscope.exc import ContainerExtractionError

    class MockFile(FilesystemFile):
        def compare_details(self, other, source=None):
            subprocess.check_output(["sh", "-c", "exit 0"])
            raise ContainerExtractionError(self.path, Exception())

    difference = MockFile(TEST_FILE1_PATH).compare(MockFile(TEST_FILE2_PATH))
    expected_diff = get_data("../data/binary_expected_diff")
    assert "Error extracting" in difference.comment
    assert normalize_zeros(difference.unified_diff) == expected_diff


@skip_unless_tools_exist("xxd")
@skip_unless_module_exists("distro")
def test_with_compare_details_and_tool_not_found(monkeypatch):
    from diffoscope.external_tools import EXTERNAL_TOOLS

    monkeypatch.setitem(
        EXTERNAL_TOOLS,
        "nonexistent",
        {
            "debian": "some-package",
            "arch": "some-package",
            "fedora": "some-package",
            "FreeBSD": "some-package",
        },
    )

    class MockFile(FilesystemFile):
        @tool_required("nonexistent")
        def compare_details(self, other, source=None):
            raise Exception("should not be run")

    difference = MockFile(TEST_FILE1_PATH).compare(MockFile(TEST_FILE2_PATH))
    expected_diff = get_data("binary_expected_diff")
    assert "nonexistent" in difference.comment
    assert "some-package" in difference.comment
    assert normalize_zeros(difference.unified_diff) == expected_diff


def test_compare_two_nonexisting_files():
    file1 = MissingFile("/nonexisting1")
    file2 = MissingFile("/nonexisting2")
    difference = file1.compare(file2)
    assert "non-existing" in difference.comment


def test_symlink_to_dir():
    # Create 2 directories, each containing sub-directory src and symbolic link dst-->src.
    with TemporaryDirectory() as basepath1:
        with TemporaryDirectory() as basepath2:
            src1path = os.path.join(basepath1, "src")
            dst1path = os.path.join(basepath1, "lnk")
            src2path = os.path.join(basepath2, "src")
            dst2path = os.path.join(basepath2, "lnk")
            mkdir(src1path)
            mkdir(src2path)
            symlink(src1path, dst1path)
            symlink(src2path, dst2path)

            # Compare these directories' content.
            file1 = FilesystemFile(basepath1)
            file2 = FilesystemFile(basepath2)
            assert file1.has_same_content_as(file2) is False
