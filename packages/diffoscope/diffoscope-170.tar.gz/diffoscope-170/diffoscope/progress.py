#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2016-2020 Chris Lamb <lamby@debian.org>
# Copyright © 2018 Paul Wise <pabs@debian.org>
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
import json
import signal
import logging

from .logging import line_eraser
from .tools import python_module_missing


logger = logging.getLogger(__name__)

try:
    import progressbar
except ImportError:
    python_module_missing("progressbar")
    progressbar = None


class ProgressLoggingHandler(logging.StreamHandler):
    def __init__(self, progressbar):
        self.progressbar = progressbar
        super().__init__()

    def emit(self, record):
        try:
            super().emit(record)
            if not getattr(self.progressbar.bar, "finished", False):
                self.progressbar.bar.update()
        except Exception:
            # Wrap otherwise tests fail due to test_progress.py call main()
            # several times. This mirrors the super() implementation.
            self.handleError(record)


class ProgressManager:
    _singleton = {}

    def __init__(self):
        self.__dict__ = self._singleton

        if not self._singleton:
            self.reset()

    def reset(self):
        self.stack = []
        self.observers = []

    def setup(self, parsed_args):
        def show_progressbar():
            # Show progress bar if user explicitly asked for it
            if parsed_args.progress:
                return True

            # ... otherwise show it if STDOUT is a tty and we are not debugging
            if parsed_args.progress is None:
                return sys.stdout.isatty() and not parsed_args.debug

            return False

        log_handler = None
        if show_progressbar():
            if progressbar is not None:
                bar = ProgressBar()
                self.register(bar)
                log_handler = ProgressLoggingHandler(bar)
            else:
                # User asked for bar, so show them an error

                if parsed_args.progress:
                    logging.warning(
                        'Progress bar was requested but the "progressbar" module is unavailable.'
                    )

        if parsed_args.status_fd:
            self.register(StatusFD(os.fdopen(parsed_args.status_fd, "w")))

        return log_handler

    def push(self, progress):
        assert not self.stack or self.stack[-1].is_active()
        self.stack.append(progress)

    def pop(self, progress):
        x = self.stack.pop()
        assert x is progress
        if self.stack:
            self.stack[-1].child_done(x.total)

    def register(self, observer):
        logger.debug("Registering %s as a progress observer", observer)
        self.observers.append(observer)

    def update(self, msg):
        if self.stack:
            cur_estimates = None
            for progress in reversed(self.stack):
                cur_estimates = progress.estimates(cur_estimates)
            current, total = cur_estimates
        else:
            current, total = 0, 1

        for x in self.observers:
            x.notify(current, total, msg)

    def finish(self):
        for x in self.observers:
            x.finish()


class Progress:
    def __init__(self, total=None):
        self.done = []
        self.current_steps = None
        self.current_child_steps_done = None
        if total:
            self.total = total
        else:
            self.total = 1
            self.begin_step(1)

    def __enter__(self):
        ProgressManager().push(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.maybe_end()
        ProgressManager().pop(self)

    def estimates(self, cur_child_estimate=None):
        own_done = sum(pair[0] for pair in self.done)
        children_done = sum(pair[1] for pair in self.done)
        all_done = own_done + children_done

        if self.current_steps:
            if self.current_child_steps_done or cur_child_estimate:
                # Something is in-progress, the calculation is slightly more
                # complex
                cur_child_done, cur_child_total = cur_child_estimate or (0, 0)
                own_done += self.current_steps
                all_done += (
                    self.current_steps
                    + self.current_child_steps_done
                    + cur_child_done
                )
                # Cost of what we expect will have been done, once the current
                # in-progress step plus all of its children, have completed
                expected_all_done = all_done + (
                    cur_child_total - cur_child_done
                )
                assert own_done  # non-zero
                return (
                    all_done,
                    int(float(self.total) / own_done * expected_all_done),
                )
        else:
            # nothing in progress
            assert not cur_child_estimate

        if not own_done:
            assert not children_done
            return 0, self.total

        # weigh self.total by (all_done/own_done)
        return all_done, int(float(self.total) / own_done * all_done)

    def is_active(self):
        return self.current_steps is not None

    def maybe_end(self, msg=""):
        if self.is_active():
            self.done += [(self.current_steps, self.current_child_steps_done)]
            self.current_steps = None
            self.current_child_steps_done = None
            ProgressManager().update(msg)

    def begin_step(self, step, msg=""):
        assert step is not None
        self.maybe_end(msg)
        self.current_steps = step
        self.current_child_steps_done = 0

    def child_done(self, total):
        self.current_child_steps_done += total


class ProgressBar:
    def __init__(self):
        try:
            from progressbar.widgets import WidgetBase
        except ImportError:
            # Fallback to the older Debian version
            from progressbar import Widget as WidgetBase

        self.msg = ""

        class Message(WidgetBase):
            def update(self, pbar, _observer=self):
                msg = _observer.msg
                width = 25

                if len(msg) <= width:
                    return msg.rjust(width)

                # Print the last `width` characters with an ellipsis.
                return "…{}".format(msg[-width + 1 :])

        class OurProgressBar(progressbar.ProgressBar):
            def __init__(self, *args, **kwargs):
                # Remove after https://github.com/niltonvolpato/python-progressbar/pull/57 is fixed.
                kwargs.setdefault("fd", sys.stderr)
                super().__init__(*args, **kwargs)
                # Terminal handling after parent init since that sets self.fd
                self.erase_to_eol = line_eraser(self.fd)

            def _need_update(self):
                return True

            def erase_line(self):
                if self.erase_to_eol:
                    self.fd.buffer.write(self.erase_to_eol)
                    self.fd.flush()

            def finish(self):
                self.finished = True
                self.update(self.maxval)
                # Clear the progress bar after completion
                self.erase_line()
                if self.signal_set:
                    signal.signal(signal.SIGWINCH, signal.SIG_DFL)

        self.bar = OurProgressBar(
            widgets=(
                " ",
                progressbar.Bar(),
                "  ",
                progressbar.Percentage(),
                "  ",
                Message(),
                "  ",
                progressbar.ETA(),
                " ",
            )
        )
        self.bar.start()

    def notify(self, current, total, msg):
        self.msg = msg

        self.bar.maxval = total
        self.bar.currval = current
        self.bar.update()

    def finish(self):
        self.bar.finish()


class StatusFD:
    def __init__(self, fileobj):
        self.fileobj = fileobj

    def notify(self, current, total, msg):
        print(
            json.dumps({"msg": msg, "total": total, "current": current}),
            file=self.fileobj,
        )

    def finish(self):
        pass
