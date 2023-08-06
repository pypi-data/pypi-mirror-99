#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2017, 2019-2020 Chris Lamb <lamby@debian.org>
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

from diffoscope.comparators.image import ICOImageFile
from diffoscope.config import Config

from ..utils.data import load_fixture, get_data
from ..utils.tools import (
    skip_unless_tools_exist,
    skip_unless_tool_is_at_least,
)
from .test_jpeg_image import identify_version


image1 = load_fixture("test1.ico")
image2 = load_fixture("test2.ico")
image1_meta = load_fixture("test1_meta.ico")
image2_meta = load_fixture("test2_meta.ico")


def test_identification(image1):
    assert isinstance(image1, ICOImageFile)


def test_no_differences(image1):
    difference = image1.compare(image1)
    assert difference is None


@pytest.fixture
def differences(image1, image2):
    return image1.compare(image2).details


@skip_unless_tools_exist("img2txt", "convert")
def test_diff(differences):
    expected_diff = get_data("ico_image_expected_diff")
    assert differences[0].unified_diff == expected_diff


@pytest.fixture
def differences_meta(image1_meta, image2_meta):
    return image1_meta.compare(image2_meta).details


@skip_unless_tools_exist("img2txt", "identify")
@skip_unless_tool_is_at_least("identify", identify_version, "6.9.10-23")
def test_diff_meta(differences_meta):
    expected_diff = get_data("ico_image_meta_expected_diff")
    assert differences_meta[-1].unified_diff == expected_diff


@skip_unless_tools_exist("img2txt", "identify")
@skip_unless_tool_is_at_least("identify", identify_version, "6.9.10-23")
def test_diff_meta2(differences_meta):
    expected_diff = get_data("ico_image_meta_expected_diff_v2")
    assert differences_meta[-1].unified_diff == expected_diff


@skip_unless_tools_exist("img2txt", "compose", "convert", "identify")
def test_has_visuals(monkeypatch, image1, image2):
    monkeypatch.setattr(Config(), "compute_visual_diffs", True)
    ico_diff = image1.compare(image2)
    assert len(ico_diff.details) == 2
    assert len(ico_diff.details[0].visuals) == 2
    assert ico_diff.details[0].visuals[0].data_type == "image/png;base64"
    assert ico_diff.details[0].visuals[1].data_type == "image/gif;base64"
