"""Recording what an algorithm does, step by step.

Library functions such as ``introai.search.expand`` call :func:`emit` to report
events ("a node was expanded", "the frontier now looks like this"). Nothing is
stored unless someone is listening: wrap a call in :func:`record` to collect
the events into a :class:`Trace`.

    with record() as trace:
        bfs(problem)
    print(len(trace.of_kind("expand")), "nodes expanded")
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Event:
    """One thing that happened, e.g. ``Event("expand", {"node": node})``."""

    kind: str
    data: dict[str, Any]


class TraceLimitExceeded(Exception):
    """Raised when a recording grows beyond its limit (usually an endless loop)."""


@dataclass
class Trace:
    """The events collected by one :func:`record` block, in order."""

    events: list[Event] = field(default_factory=list)
    limit: int | None = None
    kinds: frozenset[str] | None = None

    def of_kind(self, kind: str) -> list[Event]:
        """Return only the events of the given kind, in order."""
        return [event for event in self.events if event.kind == kind]


_current: ContextVar[Trace | None] = ContextVar("introai_current_trace", default=None)


@contextmanager
def record(limit: int | None = None, kinds: Iterable[str] | None = None) -> Iterator[Trace]:
    """Collect every event emitted inside the ``with`` block.

    ``limit`` caps the number of events; exceeding it raises
    :class:`TraceLimitExceeded`, which turns an endless loop into a quick failure.
    ``kinds`` keeps only events of those kinds (for example ``{"expand"}``); code
    that builds expensive event data can ask :func:`wants` first and skip it.
    Nested blocks record separately: the inner block sees only its own events.
    """
    trace = Trace(limit=limit, kinds=frozenset(kinds) if kinds is not None else None)
    token = _current.set(trace)
    try:
        yield trace
    finally:
        _current.reset(token)


def wants(kind: str) -> bool:
    """Whether an active recording keeps events of this kind."""
    trace = _current.get()
    return trace is not None and (trace.kinds is None or kind in trace.kinds)


def emit(kind: str, **data: Any) -> None:
    """Report an event to the active recording, if there is one."""
    trace = _current.get()
    if trace is None or (trace.kinds is not None and kind not in trace.kinds):
        return
    if trace.limit is not None and len(trace.events) >= trace.limit:
        raise TraceLimitExceeded(f"more than {trace.limit} events were recorded")
    trace.events.append(Event(kind, data))
