#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2014-2015 Jérémy Bobbio <lunar@debian.org>
# Copyright © 2016-2021 Chris Lamb <lamby@debian.org>
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

import os
import sys
import errno
import signal
import logging
import textwrap
import argparse
import traceback

from . import VERSION
from .path import set_path
from .tools import (
    get_tools,
    tool_check_installed,
    tool_prepend_prefix,
    python_module_missing,
    tool_required,
    OS_NAMES,
    get_current_os,
)
from .config import Config
from .environ import normalize_environment
from .logging import line_eraser, setup_logging
from .progress import ProgressManager, Progress
from .profiling import ProfileManager, profile
from .tempfiles import clean_all_temp_files
from .difference import Difference
from .comparators import ComparatorManager
from .external_tools import EXTERNAL_TOOLS, HUGE_TOOLS
from .presenters.html import JQUERY_SYSTEM_LOCATIONS
from .presenters.formats import PresenterManager
from .comparators.utils.compare import compare_root_paths
from .readers import load_diff, load_diff_from_path

logger = logging.getLogger(__name__)


try:
    import tlsh
except ImportError:
    python_module_missing("tlsh")
    tlsh = None

try:
    import argcomplete
except ImportError:
    python_module_missing("argcomplete")
    argcomplete = None


class BooleanAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed for BooleanAction")
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, not option_string.startswith("--no"))


def create_parser():
    parser = argparse.ArgumentParser(
        description="Calculate differences between two files or directories",
        add_help=False,
        formatter_class=HelpFormatter,
        fromfile_prefix_chars="@",
    )
    parser.add_argument(
        "path1",
        help="First file or directory to compare.",
    )
    parser.add_argument("path2", help="Second file or directory to compare.")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Display debug messages",
    )
    parser.add_argument(
        "--pdb",
        action="store_true",
        help="Open the Python pdb debugger in case of crashes",
    )
    parser.add_argument(
        "--status-fd",
        metavar="FD",
        type=int,
        help="Send machine-readable status to file descriptor FD",
    )
    parser.add_argument(
        "--progress",
        "--no-progress",
        action=BooleanAction,
        default=None,
        help="Show an approximate progress bar. Default: yes if "
        "stdin is a tty, otherwise no.",
    )
    parser.add_argument(
        "--no-default-limits",
        action="store_true",
        default=False,
        help="Disable most default output limits and diff calculation limits.",
    )

    group1 = parser.add_argument_group("output types")
    group1.add_argument(
        "--text",
        metavar="OUTPUT_FILE",
        dest="text_output",
        help="Write plain text output to given file (use - for stdout)",
    )
    group1.add_argument(
        "--text-color",
        metavar="WHEN",
        default="auto",
        choices=["never", "auto", "always"],
        help="When to output color diff. WHEN is one of {%(choices)s}. "
        "Default: auto, meaning yes if the output is a terminal, otherwise no.",
    )
    group1.add_argument(
        "--output-empty",
        action="store_true",
        help="If there was no difference, then output an empty "
        "diff for each output type that was specified. In "
        "--text output, an empty file is written.",
    )
    group1.add_argument(
        "--html",
        metavar="OUTPUT_FILE",
        dest="html_output",
        help="Write HTML report to given file (use - for stdout)",
    )
    group1.add_argument(
        "--html-dir",
        metavar="OUTPUT_DIR",
        dest="html_output_directory",
        help="Write multi-file HTML report to given directory",
    )
    group1.add_argument(
        "--css",
        metavar="URL",
        dest="css_url",
        help="Link to an extra CSS for the HTML report",
    )
    group1.add_argument(
        "--jquery",
        metavar="URL",
        dest="jquery_url",
        help="URL link to jQuery, for --html and --html-dir output. "
        "If this is a non-existent relative URL, diffoscope will create a "
        "symlink to a system installation. (Paths searched: %s.) "
        "If not given, --html output will not use JS but --html-dir will "
        'if it can be found; give "disable" to disable JS on all outputs.'
        % ", ".join(JQUERY_SYSTEM_LOCATIONS),
    )
    group1.add_argument(
        "--json",
        metavar="OUTPUT_FILE",
        dest="json_output",
        help="Write JSON text output to given file (use - for stdout)",
    )
    group1.add_argument(
        "--markdown",
        metavar="OUTPUT_FILE",
        dest="markdown_output",
        help="Write Markdown text output to given file (use - for stdout)",
    )
    group1.add_argument(
        "--restructured-text",
        metavar="OUTPUT_FILE",
        dest="restructuredtext_output",
        help="Write RsT text output to given file (use - for stdout)",
    )
    group1.add_argument(
        "--difftool",
        metavar="TOOL",
        dest="difftool",
        help="Compare differences one-by-one using the specified external "
        "command similar to git-difftool(1)",
    )
    group1.add_argument(
        "--profile",
        metavar="OUTPUT_FILE",
        dest="profile_output",
        nargs="?",
        const="-",
        default=None,
        help="Write profiling info to given file (use - for stdout)",
    )
    parser.add_argument(
        "--load-existing-diff",
        metavar="INPUT_FILE",
        action=LoadExistingDiffAction,
        dest="load_existing_diff",
        help='Load existing diff from file. Specify "-" to read a diffoscope diff from stdin.',
    )

    group2 = parser.add_argument_group("output limits")
    # everything marked with default=None below is affected by no-default-limits
    group2.add_argument(
        "--max-text-report-size",
        metavar="BYTES",
        type=int,
        help="Maximum bytes written in --text report. (0 to "
        "disable, default: %d)" % Config().max_text_report_size,
        default=None,
    )
    group2.add_argument(
        "--max-report-size",
        metavar="BYTES",
        type=int,
        help="Maximum bytes of a report in a given format, "
        "across all of its pages. Note that some formats, such "
        "as --html, may be restricted by even smaller limits "
        "such as --max-page-size. (0 to disable, default: %d)"
        % Config().max_report_size,
        default=None,
    ).completer = RangeCompleter(Config().max_report_size)
    group2.add_argument(
        "--max-diff-block-lines",
        metavar="LINES",
        type=int,
        help="Maximum number of lines output per unified-diff "
        "block, across all pages. (0 to disable, default: %d)"
        % Config().max_diff_block_lines,
        default=None,
    ).completer = RangeCompleter(Config().max_diff_block_lines)
    group2.add_argument(
        "--max-page-size",
        metavar="BYTES",
        type=int,
        help="Maximum bytes of the top-level (--html-dir) or sole "
        "(--html) page. (default: %(default)s, remains in effect "
        "even with --no-default-limits)",
        default=Config().max_page_size,
    ).completer = RangeCompleter(Config().max_page_size)
    group2.add_argument(
        "--max-page-diff-block-lines",
        metavar="LINES",
        type=int,
        help="Maximum number of lines output per unified-diff block "
        "on the top-level (--html-dir) or sole (--html) page, before "
        "spilling it into a child page (--html-dir) or skipping the "
        "rest of the diff block. (default: %(default)s, remains in "
        "effect even with --no-default-limits)",
        default=Config().max_page_diff_block_lines,
    ).completer = RangeCompleter(Config().max_page_diff_block_lines)

    group3 = parser.add_argument_group("diff calculation")
    group3.add_argument(
        "--new-file", action="store_true", help="Treat absent files as empty"
    )
    group3.add_argument(
        "--exclude",
        dest="excludes",
        metavar="GLOB_PATTERN",
        action="append",
        default=[],
        help="Exclude files whose names (including any directory part) "
        "match %(metavar)s. Use this option to ignore files based on "
        "their names.",
    )
    group3.add_argument(
        "--exclude-command",
        dest="exclude_commands",
        metavar="REGEX_PATTERN",
        action="append",
        default=[],
        help="Exclude commands that match %(metavar)s. For "
        "example '^readelf.*\\s--debug-dump=info' and '^radare2.*' can take"
        "a long time and differences here are likely secondary differences "
        "caused by something represented elsewhere. Use this option to "
        "disable commands that use a lot of resources.",
    )
    group3.add_argument(
        "--exclude-directory-metadata",
        choices=("auto", "yes", "no", "recursive"),
        help="Exclude directory metadata. Useful if comparing "
        "files whose filesystem-level metadata is not intended "
        "to be distributed to other systems. This is true for "
        "most distributions package builders, but not true "
        "for the output of commands such as `make install`. "
        "Metadata of archive members remain un-excluded "
        'except if "recursive" choice is set. '
        "Use this option to ignore permissions, timestamps, "
        "xattrs etc. Default: 'no' if comparing two "
        "directories, else 'yes'. Note that \"file\" metadata is "
        "actually a property of its containing directory "
        "and is not relevant when distributing the file across "
        "systems.",
    )
    group3.add_argument(
        "--extended-filesystem-attributes",
        "--no-extended-filesystem-attributes",
        action=BooleanAction,
        default=False,
        help="Check potentially-expensive filesystem extended "
        "attributes such as POSIX ACLs, lsattr(1)/chattr(1) "
        "attributes etc. (default: False)",
    )
    group3.add_argument(
        "--diff-mask",
        metavar="REGEX_PATTERN",
        dest="diff_masks",
        action="append",
        default=[],
        help="Replace/unify substrings that match regular expression "
        "%(metavar)s from output strings before applying diff. For example, to "
        "filter out a version number or changed path.",
    )
    group3.add_argument(
        "--fuzzy-threshold",
        type=int,
        help="Threshold for fuzzy-matching "
        "(0 to disable, %(default)s is default, 400 is high fuzziness)",
        default=Config().fuzzy_threshold,
    ).completer = RangeCompleter(400)
    group3.add_argument(
        "--tool-prefix-binutils",
        metavar="PREFIX",
        help="Prefix for binutils program names, e.g. "
        '"aarch64-linux-gnu-" for a foreign-arch binary or "g" '
        "if you're on a non-GNU system.",
    )
    group3.add_argument(
        "--max-diff-input-lines",
        metavar="LINES",
        type=int,
        help="Maximum number of lines fed to diff(1) "
        "(0 to disable, default: %d)" % Config().max_diff_input_lines,
        default=None,
    ).completer = RangeCompleter(Config().max_diff_input_lines)
    group3.add_argument(
        "--max-container-depth",
        metavar="DEPTH",
        type=int,
        help="Maximum depth to recurse into containers. "
        "(Cannot be disabled for security reasons, default: "
        "%(default)s)",
        default=Config().max_container_depth,
    )
    group3.add_argument(
        "--max-diff-block-lines-saved",
        metavar="LINES",
        type=int,
        help="Maximum number of lines saved per diff block. "
        "Most users should not need this, unless you run out "
        "of memory. This truncates diff(1) output before emitting "
        "it in a report, and affects all types of output, "
        "including --text and --json. (0 to disable, default: "
        "%(default)s)",
        default=0,
    )
    group3.add_argument(
        "--use-dbgsym",
        metavar="WHEN",
        default="auto",
        choices=("no", "auto", "yes"),
        help="When to automatically use corresponding -dbgsym packages when "
        "comparing .deb files. WHEN is one of {%(choices)s}. Default: auto, "
        "meaning yes if two .changes or .buildinfo files are specified, "
        "otherwise no.",
    )
    group3.add_argument(
        "--force-details",
        default=False,
        action="store_true",
        help="Force recursing into the depths of file formats "
        "even if files have the same content, only really "
        "useful for debugging diffoscope. Default: %(default)s",
    )

    group4 = parser.add_argument_group("information commands")
    group4.add_argument(
        "--help", "-h", action="help", help="Show this help and exit"
    )
    group4.add_argument(
        "--version",
        action="version",
        version="diffoscope %s" % VERSION,
        help="Show program's version number and exit",
    )
    group4.add_argument(
        "--list-tools",
        nargs="?",
        type=str,
        action=ListToolsAction,
        metavar="DISTRO",
        choices=OS_NAMES,
        help="Show external tools required and exit. "
        "DISTRO can be one of {%(choices)s}. "
        "If specified, the output will list packages in that "
        "distribution that satisfy these dependencies.",
    )
    group4.add_argument(
        "--list-debian-substvars",
        action=ListDebianSubstvarsAction,
        help="List packages needed for Debian in 'substvar' format.",
    )
    group4.add_argument(
        "--list-missing-tools",
        nargs="?",
        type=str,
        action=ListMissingToolsAction,
        metavar="DISTRO",
        choices=OS_NAMES,
        help="Show missing external tools and exit. "
        "DISTRO can be one of {%(choices)s}. "
        "If specified, the output will list packages in that "
        "distribution that satisfy these dependencies.",
    )

    if not tlsh:
        parser.epilog = (
            "File renaming detection based on fuzzy-matching is currently "
            'disabled. It can be enabled by installing the "tlsh" module '
            "available from https://github.com/trendmicro/tlsh or in the "
            "python3-tlsh package."
        )
    if argcomplete:
        argcomplete.autocomplete(parser)
    elif "_ARGCOMPLETE" in os.environ:
        logger.error(
            'Argument completion requested but the "argcomplete" module is '
            "not installed. It can be obtained from "
            "https://pypi.python.org/pypi/argcomplete or in the "
            "python3-argcomplete package."
        )
        sys.exit(1)

    def post_parse(parsed_args):
        if parsed_args.load_existing_diff is not None:
            # warn about unusual flags in this mode
            ineffective_flags = [
                f
                for x in group3._group_actions
                if getattr(parsed_args, x.dest) != x.default
                for f in x.option_strings
            ]
            if ineffective_flags:
                logger.warning(
                    "Loading diff instead of calculating it, but "
                    "diff-calculation flags were given; they will be ignored:"
                )
                logger.warning(ineffective_flags)

    return parser, post_parse


class HelpFormatter(argparse.HelpFormatter):
    def format_help(self, *args, **kwargs):
        val = super().format_help(*args, **kwargs)

        # Only append the file formats if --help is passed.
        if not set(sys.argv) & {"--help", "-h"}:
            return val

        def append(title, content, indent=24, max_width=78):
            nonlocal val
            wrapped = textwrap.fill(content, max_width - indent)
            val += "\n{}:\n{}\n".format(
                title, textwrap.indent(wrapped, " " * indent)
            )

        append(
            "file formats supported",
            ComparatorManager().format_descriptions(),
        )

        append("diffoscope homepage", "<https://diffoscope.org/>")

        append(
            "bugs/issues",
            "<https://salsa.debian.org/reproducible-builds/diffoscope/issues>",
            max_width=sys.maxsize,
        )

        return val


class RangeCompleter:
    def __init__(self, start, end=0, divisions=16):
        if end < start:
            tmp = end
            end = start
            start = tmp
        self.choices = range(
            start, end + 1, int((end - start + 1) / divisions)
        )

    def __call__(self, prefix, **kwargs):
        return (str(i) for i in self.choices if str(i).startswith(prefix))


class LoadExistingDiffAction(argparse._StoreAction):
    def __call__(self, parser, *args, **kwargs):
        actions_by_dest = {x.dest: x for x in parser._actions}

        # If we have passed a value for --load_existing_diff we don't require
        # path1 or path2 anymore.
        actions_by_dest["path1"].required = False
        actions_by_dest["path2"].required = False

        # Actually store the value.
        super().__call__(parser, *args, **kwargs)


class ListToolsAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.only_missing = False

    def __call__(self, parser, namespace, os_override, option_string=None):
        # Ensure all comparators are imported so tool_required.all is
        # populated.
        ComparatorManager().reload()

        for k, v in sorted(get_tools(self.only_missing).items()):
            print("%s: %s" % (k, ", ".join(v)))

        sys.exit(0)


class ListMissingToolsAction(ListToolsAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.only_missing = True


class ListDebianSubstvarsAction(argparse._StoreTrueAction):
    def __call__(self, *args, **kwargs):
        # Attempt to import all comparators so tool_required.all is as
        # populated as possible...
        ComparatorManager().reload()

        # ... however for the generated substvar to be effective/deterministic
        # regardless of the currently installed packages, we special-case some
        # tools (NB. not package names) as their modules may not have been
        # imported by the `ComparatorManager().reload()` call above. (#908072)
        tools = set(
            ("gpg", "rpm2cpio")  # comparators/debian.py  # comparators/rpm.py
        )
        tools.update(tool_required.all)

        packages = set()
        packages_minimal = set()
        for x in tools:
            try:
                pkg = EXTERNAL_TOOLS[x]["debian"]
            except KeyError:
                continue

            packages.add(pkg)
            if x not in HUGE_TOOLS:
                packages_minimal.add(pkg)

        # Exclude "Required" packages
        for x in ("gzip", "tar", "coreutils", "diffutils", "findutils"):
            packages.discard(x)
            packages_minimal.discard(x)

        description = "File formats supported include: {}".format(
            ComparatorManager().format_descriptions(),
        )
        wrapped = "${Newline}".join(textwrap.wrap(description, 79))
        wrapped = wrapped.replace("${Newline}.", "${Newline}")
        print("diffoscope:Description={}".format(wrapped))

        print("diffoscope:Recommends={}".format(", ".join(sorted(packages))))
        print(
            "diffoscope-minimal:Recommends={}".format(
                ", ".join(sorted(packages_minimal))
            )
        )

        sys.exit(0)


def configure(parsed_args):
    for x in (
        "max_report_size",
        "max_text_report_size",
        "max_diff_block_lines",
        "max_diff_block_lines_saved",
        "max_diff_input_lines",
    ):
        # Apply limits affected by "no-default-limits"
        v = getattr(parsed_args, x)
        if v is not None:
            setattr(Config(), x, float("inf") if v == 0 else v)

        elif parsed_args.no_default_limits:
            setattr(Config(), x, float("inf"))

    Config().max_page_size = parsed_args.max_page_size
    Config().max_page_diff_block_lines = parsed_args.max_page_diff_block_lines

    Config().difftool = parsed_args.difftool
    Config().new_file = parsed_args.new_file
    Config().use_dbgsym = parsed_args.use_dbgsym
    Config().force_details = parsed_args.force_details
    Config().fuzzy_threshold = parsed_args.fuzzy_threshold
    Config().max_container_depth = parsed_args.max_container_depth

    Config().excludes = parsed_args.excludes
    Config().exclude_commands = parsed_args.exclude_commands
    Config().exclude_directory_metadata = (
        parsed_args.exclude_directory_metadata
    )
    Config().extended_filesystem_attributes = (
        parsed_args.extended_filesystem_attributes
    )
    Config().diff_masks = parsed_args.diff_masks

    Config().compute_visual_diffs = PresenterManager().compute_visual_diffs()

    tool_prepend_prefix(
        parsed_args.tool_prefix_binutils,
        "ar",
        "as",
        "ld",
        "ld.bfd",
        "nm",
        "objcopy",
        "objdump",
        "ranlib",
        "readelf",
        "strip",
    )

    Config().check_constraints()


def run_diffoscope(parsed_args):
    """
    (This should not be considered a stable API suitable for external
    consumption, and the lack of configuration of globals may result in
    unpredictable behaviour.)
    """

    logger.debug("Starting diffoscope %s", VERSION)

    ProfileManager().setup(parsed_args)
    PresenterManager().configure(parsed_args)
    if not tlsh and "PYTEST_CURRENT_TEST" not in os.environ:
        logger.info(
            'Fuzzy-matching is currently disabled as the "tlsh" module is unavailable.'
        )

    configure(parsed_args)
    set_path()
    normalize_environment()

    path1, path2 = parsed_args.path1, parsed_args.path2

    # Should we be loading an existing diff from a file
    if parsed_args.load_existing_diff:
        x = parsed_args.load_existing_diff

        if x == "-":
            logger.debug("Loading diff from stdin")
            difference = load_diff(sys.stdin, "stdin")
        else:
            logger.debug(
                "Loading diff from %s", parsed_args.load_existing_diff
            )
            difference = load_diff_from_path(x)
    else:
        if Config().exclude_directory_metadata in ("auto", None):
            # Default to ignoring metadata directory...
            Config().exclude_directory_metadata = "yes"
            if os.path.isdir(path1) and os.path.isdir(path2):
                # ... except if we passed two directories.
                Config().exclude_directory_metadata = "no"

        logger.debug("Starting comparison")
        with Progress():
            with profile("main", "outputs"):
                difference = compare_root_paths(path1, path2)
        ProgressManager().finish()
    # Generate an empty, null diff to write, saving the exit code first.
    has_differences = bool(difference is not None)
    if difference is None and parsed_args.output_empty:
        difference = Difference(None, path1, path2)
    with profile("main", "outputs"):
        PresenterManager().output(difference, parsed_args, has_differences)
    return 1 if has_differences else 0


def sigterm_handler(signo, stack_frame):
    clean_all_temp_files()
    os._exit(2)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        import libarchive  # noqa
    except (ImportError, AttributeError):
        traceback.print_exc()
        python_module_missing("libarchive")
        print(
            "\nMissing or incomplete libarchive module. Try installing your "
            "system's 'libarchive' package.",
            file=sys.stderr,
        )
        sys.exit(2)

    parsed_args = None

    try:
        with profile("main", "parse_args"):
            parser, post_parse = create_parser()
            parsed_args = parser.parse_args(args)

        log_handler = ProgressManager().setup(parsed_args)

        with setup_logging(parsed_args.debug, log_handler) as logger:
            post_parse(parsed_args)

            # Call main entry point
            sys.exit(run_diffoscope(parsed_args))

    except BrokenPipeError:
        sys.exit(2)
    except OSError as e:
        if e.errno != errno.ENOSPC:
            raise
        logger.error("No space left on device. Diffoscope exiting.")
        sys.exit(2)
    except KeyboardInterrupt:
        logger.error("Keyboard Interrupt")
        sys.exit(2)
    except Exception:
        sys.stderr.buffer.write(line_eraser())
        traceback.print_exc()
        if parsed_args and parsed_args.pdb:
            import pdb

            pdb.post_mortem()
        sys.exit(2)
    finally:
        # Helps our tests run more predictably - some of them call main()
        # which sets Config() values.
        Config().reset()

        with profile("main", "cleanup"):
            clean_all_temp_files()

        # Print profiling output at the very end
        if parsed_args is not None:
            ProfileManager().finish(parsed_args)


if __name__ == "__main__":
    main()
