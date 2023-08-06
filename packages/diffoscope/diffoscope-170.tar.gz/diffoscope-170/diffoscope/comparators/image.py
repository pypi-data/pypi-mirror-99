#
# diffoscope: in-depth comparison of files, archives, and directories
#
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

import re
import base64
import logging
import subprocess

from diffoscope.config import Config
from diffoscope.tools import tool_required
from diffoscope.tempfiles import get_named_temporary_file
from diffoscope.difference import Difference, VisualDifference

from .utils.file import File
from .utils.command import Command, our_check_output

re_ansi_escapes = re.compile(r"\x1b[^m]*m")

logger = logging.getLogger(__name__)


class Img2Txt(Command):
    @tool_required("img2txt")
    def cmdline(self):
        return ["img2txt", "--width", "60", "--format", "utf8", self.path]

    def filter(self, line):
        # Strip ANSI escapes
        return re_ansi_escapes.sub("", line.decode("utf-8")).encode("utf-8")


class Identify(Command):
    ATTRIBUTES = (
        "Image format: %m",
        "File size: %b",
        "Height: %[height]",
        "Width: %[width]",
        "Orientation: %[orientation]",
        "Compression type: %[compression]",
        "Compression quality: %[quality]",
        "Colorspace: %[colorspace]",
        "Channels: %[channels]",
        "Depth: %[depth]",
        "Interlace mode: %[interlace]",
        "Rendering intent: %[rendering-intent]",
        "X resolution: %[resolution.x]",
        "Y resolution: %[resolution.y]",
        "Resolution units: %[units]",
        "Transparency channel enabled: %A",
        "Gamma: %[gamma]",
        "Number of unique colors: %[colors]",
        "Comment: %c",
        "EXIF data: %[EXIF:*]",
    )

    @tool_required("identify")
    def cmdline(self):
        return ["identify", "-format", "\n".join(self.ATTRIBUTES), self.path]


@tool_required("compare")
def pixel_difference(image1_path, image2_path):
    compared_filename = get_named_temporary_file(suffix=".png").name

    try:
        our_check_output(
            (
                "compare",
                image1_path,
                image2_path,
                "-compose",
                "src",
                compared_filename,
            )
        )
    except subprocess.CalledProcessError as e:
        # ImageMagick's `compare` will return 1 if images are different
        if e.returncode == 1:
            pass

    with open(compared_filename, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")

    return VisualDifference("image/png;base64", content, "Pixel difference")


@tool_required("convert")
def flicker_difference(image1_path, image2_path):
    compared_filename = get_named_temporary_file(suffix=".gif").name

    our_check_output(
        (
            "convert",
            "-delay",
            "50",
            image1_path,
            image2_path,
            "-loop",
            "0",
            "-compose",
            "difference",
            compared_filename,
        )
    )

    with open(compared_filename, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")

    return VisualDifference("image/gif;base64", content, "Flicker difference")


@tool_required("identify")
def get_image_size(image_path):
    return our_check_output(("identify", "-format", "%[h]x%[w]", image_path))


def same_size(image1, image2):
    try:
        return get_image_size(image1.path) == get_image_size(image2.path)
    except subprocess.CalledProcessError:  # noqa
        return False


class JPEGImageFile(File):
    DESCRIPTION = "JPEG images"
    FILE_TYPE_RE = re.compile(r"\bJPEG image data\b")

    def compare_details(self, other, source=None):
        content_diff = Difference.from_operation(
            Img2Txt, self.path, other.path, source="Image content"
        )
        if (
            content_diff is not None
            and Config().compute_visual_diffs
            and same_size(self, other)
        ):
            try:
                logger.debug(
                    "Generating visual difference for %s and %s",
                    self.path,
                    other.path,
                )
                content_diff.add_visuals(
                    [
                        pixel_difference(self.path, other.path),
                        flicker_difference(self.path, other.path),
                    ]
                )
            except subprocess.CalledProcessError:  # noqa
                pass
        return [
            content_diff,
            Difference.from_operation(
                Identify, self.path, other.path, source="Image metadata"
            ),
        ]


class ICOImageFile(File):
    DESCRIPTION = "Microsoft Windows icon files"
    FILE_TYPE_RE = re.compile(r"\bMS Windows icon resource\b")

    def compare_details(self, other, source=None):
        differences = []

        # img2txt does not support .ico files directly so convert to .PNG.
        try:
            png_a, png_b = [ICOImageFile.convert(x) for x in (self, other)]
        except subprocess.CalledProcessError:  # noqa
            pass
        else:
            content_diff = Difference.from_operation(
                Img2Txt, png_a, png_b, source="Image content"
            )
            if (
                content_diff is not None
                and Config().compute_visual_diffs
                and same_size(self, other)
            ):
                if get_image_size(self.path) == get_image_size(other.path):
                    logger.debug(
                        "Generating visual difference for %s and %s",
                        self.path,
                        other.path,
                    )
                    content_diff.add_visuals(
                        [
                            pixel_difference(self.path, other.path),
                            flicker_difference(self.path, other.path),
                        ]
                    )
            differences.append(content_diff)

        differences.append(
            Difference.from_operation(
                Identify, self.path, other.path, source="Image metadata"
            )
        )

        return differences

    @staticmethod
    @tool_required("convert")
    def convert(file):
        result = get_named_temporary_file(suffix=".png").name

        our_check_output(("convert", file.path, result))

        return result
