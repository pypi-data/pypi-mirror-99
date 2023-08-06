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

from diffoscope.comparators.pdf import PdfFile

from ..utils.data import load_fixture, get_data
from ..utils.tools import skip_unless_tools_exist, skip_unless_module_exists
from ..utils.nonexisting import assert_non_existing


pdf1 = load_fixture("test1.pdf")
pdf2 = load_fixture("test2.pdf")
pdf1a = load_fixture("test_weird_non_unicode_chars1.pdf")
pdf2a = load_fixture("test_weird_non_unicode_chars2.pdf")


def test_identification(pdf1):
    assert isinstance(pdf1, PdfFile)


def test_no_differences(pdf1):
    difference = pdf1.compare(pdf1)
    assert difference is None


def test_differences_found_with_weird_encoding(pdf1a, pdf2a):
    # diffoscope used to crash here due to weird encoding
    difference = pdf1a.compare(pdf2a)
    assert difference


@pytest.fixture
def differences(pdf1, pdf2):
    return pdf1.compare(pdf2).details


@skip_unless_tools_exist("pdftotext")
def test_text_diff(differences):
    expected_diff = get_data("pdf_text_expected_diff")
    assert differences[0].unified_diff == expected_diff


@skip_unless_tools_exist("pdftotext")
def test_compare_non_existing(monkeypatch, pdf1):
    assert_non_existing(monkeypatch, pdf1, has_null_source=False)


@pytest.fixture
def differences_metadata(pdf1, pdf1a):
    return pdf1.compare(pdf1a).details


@skip_unless_tools_exist("pdftotext")
@skip_unless_module_exists("PyPDF2")
def test_metadata(differences_metadata):
    expected_diff = get_data("pdf_metadata_expected_diff")
    assert differences_metadata[0].unified_diff == expected_diff
