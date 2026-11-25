"""Pytest plugin that lets lesson tests run against different implementations.

Lesson tests use the ``impl`` fixture instead of importing ``task`` directly.
By default it is your ``task.py``; ``--impl`` selects another file (see
:func:`introai.testing.impl.resolve_impl_path`).
"""

from __future__ import annotations

from pathlib import Path
from types import ModuleType

import pytest

from introai.testing.impl import load_module, resolve_impl_path


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--impl",
        default="task",
        help=(
            "implementation the lesson tests load: task (default, your task.py), "
            "solution, mutant:<name> or alternative:<name>"
        ),
    )


LESSON_HINT = (
    "This ran the course's own tests (tests/), not a lesson. To check a lesson, run:\n"
    "    uv run pytest modules/<module>/<lesson>"
)


def pytest_terminal_summary(terminalreporter, exitstatus, config: pytest.Config) -> None:
    """After a bare ``pytest`` from the repository root, say how to check a lesson."""
    if config.args_source == pytest.Config.ArgsSource.TESTPATHS:
        terminalreporter.write_line("")
        for line in LESSON_HINT.splitlines():
            terminalreporter.write_line(line)


@pytest.fixture(scope="module")
def impl_path(request: pytest.FixtureRequest) -> Path:
    """The file the lesson's tests run against."""
    return resolve_impl_path(
        Path(request.path).parent,
        request.config.getoption("--impl"),
        request.config.rootpath,
    )


@pytest.fixture(scope="module")
def impl(impl_path: Path) -> ModuleType:
    """The loaded implementation module (by default the lesson's ``task.py``)."""
    return load_module(impl_path)
