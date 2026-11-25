"""Shared test setup: headless, isolated matplotlib that cleans up after itself."""

import atexit
import os
import shutil
import tempfile

_MPL_DIR = tempfile.mkdtemp(prefix="introai-mpl-")
atexit.register(shutil.rmtree, _MPL_DIR, ignore_errors=True)
os.environ["MPLBACKEND"] = "Agg"
os.environ["MPLCONFIGDIR"] = _MPL_DIR

from pathlib import Path  # noqa: E402

import pytest  # noqa: E402

_FAKE_FILES = {
    "pyproject.toml": '[tool.pytest.ini_options]\naddopts = ["--import-mode=importlib"]\n',
    "conftest.py": 'pytest_plugins = ["introai.testing.plugin"]\n',
    "modules/99_fake/01_add/test_task.py": (
        "def test_add(impl):\n"
        "    assert impl.add(2, 3) == 5\n\n\n"
        "def test_add_negative(impl):\n"
        "    assert impl.add(-1, -1) == -2\n"
    ),
    "modules/99_fake/01_add/task.py": (
        "def add(a, b):\n    raise NotImplementedError('TODO: implement add')\n"
    ),
    "solutions/99_fake/01_add/task.py": "def add(a, b):\n    return a + b\n",
    "solutions/99_fake/01_add/mutants/off_by_one.py": (
        '"""Adds one too many."""\n\n'
        'CAUGHT_BY = ("test_add", "test_add_negative")\n\n\n'
        "def add(a, b):\n    return a + b + 1\n"
    ),
    "solutions/99_fake/01_add/mutants/abs_bug.py": (
        '"""Ignores signs."""\n\n'
        'CAUGHT_BY = ("test_add_negative",)\n\n\n'
        "def add(a, b):\n    return abs(a) + abs(b)\n"
    ),
    "solutions/99_fake/01_add/alternatives/sum_list.py": (
        "def add(a, b):\n    return sum([a, b])\n"
    ),
}


@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    """A tiny course repository with one lesson, its solution, mutants and an alternative."""
    for relative, content in _FAKE_FILES.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return tmp_path
