#
# diffoscope: in-depth comparison of files, archives, and directories
#
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

import logging

from diffoscope.profiling import profile

from ...utils import format_class

from .. import ComparatorManager

logger = logging.getLogger(__name__)


def try_recognize(file, cls, recognizes):
    if isinstance(file, cls):
        return True

    # Does this file class match?
    with profile("recognizes", file):
        # logger.debug("trying %s on %s", cls, file)
        if not recognizes(file):
            return False

    # Found a match; perform type magic
    logger.debug(
        "Using %s for %s",
        format_class(cls, strip="diffoscope.comparators."),
        file.name,
    )
    new_cls = type(cls.__name__, (cls, type(file)), {})
    file.__class__ = new_cls

    return True


def specialize(file):
    for cls in ComparatorManager().classes:
        if try_recognize(file, cls, cls.recognizes):
            return file

    for cls in ComparatorManager().classes:
        if try_recognize(file, cls, cls.fallback_recognizes):
            logger.debug(
                "File recognized by fallback. Magic says: %s",
                file.magic_file_type,
            )
            return file

    logger.debug(
        "%s not identified by any comparator. Magic says: %s",
        file.name,
        file.magic_file_type,
    )

    return file


def is_direct_instance(file, cls):
    # is_direct_instance(<GzipFile>, GzipFile) == True, but
    # is_direct_instance(<IpkFile>, GzipFile) == False
    if not isinstance(file, cls):
        return False
    for c in ComparatorManager().classes:
        if c is not cls and isinstance(file, c):
            return False
    return True
