"""Choosing and loading the implementation a lesson's tests run against.

Students never need this: by default the tests load the lesson's ``task.py``.
Maintainers pass ``--impl`` to run the same tests against the reference
solution, a mutant (a deliberately broken copy) or an alternative (another
correct implementation) stored under ``solutions/``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

_EXPECTED = "expected task, solution, mutant:<name> or alternative:<name>"


def resolve_impl_path(lesson_dir: Path, impl: str, repo_root: Path) -> Path:
    """Return the file that ``--impl=<impl>`` selects for the lesson in ``lesson_dir``."""
    kind, _, name = impl.partition(":")
    valid = impl in ("task", "solution") or (kind in ("mutant", "alternative") and name)
    if not valid:
        raise ValueError(f"unknown --impl value {impl!r}; {_EXPECTED}")

    lesson_dir = Path(lesson_dir).resolve()
    if impl == "task":
        path = lesson_dir / "task.py"
    else:
        repo_root = Path(repo_root).resolve()
        solution_dir = repo_root / "solutions" / lesson_dir.relative_to(repo_root / "modules")
        if impl == "solution":
            path = solution_dir / "task.py"
        elif kind == "mutant":
            path = solution_dir / "mutants" / f"{name}.py"
        else:
            path = solution_dir / "alternatives" / f"{name}.py"

    if not path.is_file():
        raise FileNotFoundError(f"implementation file not found: {path}")
    return path


def load_module(path: Path) -> ModuleType:
    """Execute ``path`` as a fresh module with a name unique to that file."""
    path = Path(path).resolve()
    name = "introai_impl_" + hashlib.sha1(str(path).encode()).hexdigest()[:12]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
