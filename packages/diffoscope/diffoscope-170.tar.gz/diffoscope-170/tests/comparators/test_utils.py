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

import codecs
import os
import pytest
import threading

from diffoscope.config import Config
from diffoscope.difference import Difference
from diffoscope.comparators.utils.command import Command

from ..utils.data import data, load_fixture
from ..utils.tools import (
    tools_missing,
    skip_unless_tools_exist,
    skip_unless_module_exists,
)


fuzzy_tar1 = load_fixture("fuzzy1.tar")
fuzzy_tar2 = load_fixture("fuzzy2.tar")
fuzzy_tar3 = load_fixture("fuzzy3.tar")


def test_tools_missing():
    assert tools_missing() is True
    assert tools_missing("/missing") is True
    for x in ["cat", "sh"]:
        assert tools_missing(x) is False


@skip_unless_tools_exist()
def test_skip_unless_tools_exist_empty():
    pytest.xfail("Test should always be skipped")


@skip_unless_tools_exist("/missing")
def test_skip_unless_tools_exist_missing():
    pytest.xfail("Test should always be skipped")


def skip_unless_tool_is_at_least():
    func = skip_unless_tool_is_at_least
    assert func("/missing", 1, 1).name == "skip"
    # pytest.skipif().args[0] contains the evaluated statement
    assert func("cat", 1, 1).args[0] is False
    assert func("cat", 1, "1.2d.45+b8").args[0] is True

    def version():
        return "4.3-git"

    assert func("cat", version, "4.3").args[0] is False


@skip_unless_module_exists("tlsh")
def test_fuzzy_matching(fuzzy_tar1, fuzzy_tar2):
    differences = fuzzy_tar1.compare(fuzzy_tar2).details
    expected_diff = codecs.open(
        data("text_iso8859_expected_diff"), encoding="utf-8"
    ).read()
    assert differences[1].source1 == "./matching"
    assert differences[1].source2 == "./fuzzy"
    assert "similar" in differences[1].comment
    assert differences[1].unified_diff == expected_diff


@skip_unless_module_exists("tlsh")
def test_fuzzy_matching_only_once(fuzzy_tar1, fuzzy_tar3):
    differences = fuzzy_tar1.compare(fuzzy_tar3).details
    assert len(differences) == 2


fuzzy_tar_in_tar1 = load_fixture("fuzzy-tar-in-tar1.tar")
fuzzy_tar_in_tar2 = load_fixture("fuzzy-tar-in-tar2.tar")


@skip_unless_module_exists("tlsh")
def test_no_fuzzy_matching(monkeypatch, fuzzy_tar_in_tar1, fuzzy_tar_in_tar2):
    monkeypatch.setattr(Config(), "fuzzy_threshold", 0)
    difference = fuzzy_tar_in_tar1.compare(fuzzy_tar_in_tar2)
    assert len(difference.details) == 1
    assert difference.details[0].source1 == "file list"


@skip_unless_module_exists("tlsh")
def test_no_fuzzy_matching_new_file(
    monkeypatch, fuzzy_tar_in_tar1, fuzzy_tar_in_tar2
):
    monkeypatch.setattr(Config(), "fuzzy_threshold", 0)
    monkeypatch.setattr(Config(), "new_file", True)
    difference = fuzzy_tar_in_tar1.compare(fuzzy_tar_in_tar2)
    assert len(difference.details) == 3
    assert difference.details[1].source2 == "/dev/null"
    assert difference.details[2].source1 == "/dev/null"


@skip_unless_tools_exist("tee")
def test_trim_stderr_in_command():
    class FillStderr(Command):
        def cmdline(self):
            return ["tee", "/dev/stderr"]

        def stdin(self):
            r, w = os.pipe()
            r, w = os.fdopen(r), os.fdopen(w, "w")

            def write():
                for _ in range(0, Command.MAX_STDERR_LINES + 1):
                    w.write("error {}\n".format(self.path))

            threading.Thread(target=write).start()

            return r

    difference = Difference.from_operation(FillStderr, "dummy1", "dummy2")
    assert (
        "[ truncated after {} lines; 1 ignored ]".format(
            Command.MAX_STDERR_LINES
        )
        in difference.comment
    )
