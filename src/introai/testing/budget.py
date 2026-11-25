"""A step budget that turns an endless loop in student code into a quick failure.

``record(limit=...)`` stops searches that keep calling ``expand``; a loop that
never calls it (for example one that peeks at the frontier instead of removing
a node) would hang forever. :func:`step_budget` counts the lines executed in
one source file and raises :class:`StepBudgetExceeded` once there are too
many. It uses ``sys.settrace``, so it works on every operating system.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator
from contextlib import contextmanager


class StepBudgetExceeded(Exception):
    """Code in the watched file executed more lines than its budget allows."""


@contextmanager
def step_budget(filename: str, max_lines: int) -> Iterator[None]:
    """Raise :class:`StepBudgetExceeded` once ``filename`` runs more than ``max_lines`` lines."""
    count = 0

    def local_trace(frame, event, arg):
        nonlocal count
        if event == "line":
            count += 1
            if count > max_lines:
                raise StepBudgetExceeded(f"more than {max_lines} lines executed in {filename}")
        return local_trace

    def global_trace(frame, event, arg):
        return local_trace if frame.f_code.co_filename == filename else None

    previous = sys.gettrace()
    sys.settrace(global_trace)
    try:
        yield
    finally:
        sys.settrace(previous)
