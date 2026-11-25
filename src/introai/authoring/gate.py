"""The lesson gate: proof that a lesson's tests do their job.

For every lesson (a directory under ``modules/`` with a ``test_task.py``) the
same tests must:

1. reject the untouched starter ``task.py`` (pytest exit code 1, no crash);
2. accept the reference solution;
3. reject every mutant, failing at least the tests listed in its ``CAUGHT_BY``;
4. accept every alternative correct implementation.
"""

from __future__ import annotations

import argparse
import ast
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PytestResult:
    exit_code: int
    failed: frozenset[str]
    passed: frozenset[str]


def discover_lessons(repo_root: Path) -> list[Path]:
    """Lesson directories: those under ``modules/`` that contain ``test_task.py``."""
    modules = Path(repo_root) / "modules"
    if not modules.is_dir():
        return []
    return sorted(test.parent for test in modules.rglob("test_task.py"))


def read_caught_by(path: Path) -> tuple[str, ...]:
    """The ``CAUGHT_BY`` tuple of a mutant file, read without importing it."""
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "CAUGHT_BY" for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            return tuple(value)
    return ()


def run_lesson_tests(lesson_dir: Path, impl: str, repo_root: Path) -> PytestResult:
    """Run a lesson's tests against one implementation in a separate process."""
    with tempfile.TemporaryDirectory(prefix="introai-gate-") as tmp:
        junit = Path(tmp) / "junit.xml"
        command = [
            sys.executable,
            "-m",
            "pytest",
            str(lesson_dir),
            f"--impl={impl}",
            "-q",
            "-p",
            "no:cacheprovider",
            "-p",
            "introai.testing.plugin",
            "--import-mode=importlib",
            f"--rootdir={repo_root}",
            f"--junitxml={junit}",
        ]
        completed = subprocess.run(command, cwd=repo_root, capture_output=True, text=True)
        failed: set[str] = set()
        passed: set[str] = set()
        if junit.exists():
            for case in ET.parse(junit).getroot().iter("testcase"):
                name = case.get("name", "")
                if case.find("failure") is not None or case.find("error") is not None:
                    failed.add(name)
                elif case.find("skipped") is None:
                    passed.add(name)
    return PytestResult(completed.returncode, frozenset(failed), frozenset(passed))


def _matches(test: str, names: frozenset[str]) -> bool:
    return any(name == test or name.startswith(test + "[") for name in names)


def gate_lesson(lesson_dir: Path, repo_root: Path) -> list[str]:
    """Check one lesson; return a list of problems (empty when the lesson passes)."""
    lesson_dir = Path(lesson_dir).resolve()
    repo_root = Path(repo_root).resolve()
    relative = lesson_dir.relative_to(repo_root / "modules")
    label = f"modules/{relative.as_posix()}"
    solution_dir = repo_root / "solutions" / relative
    problems: list[str] = []

    starter = run_lesson_tests(lesson_dir, "task", repo_root)
    if starter.exit_code != 1:
        problems.append(
            f"{label}: starter: expected failing tests (exit 1), got exit {starter.exit_code}"
        )

    solution = run_lesson_tests(lesson_dir, "solution", repo_root)
    if solution.exit_code != 0:
        problems.append(
            f"{label}: solution: expected all tests to pass (exit 0), "
            f"got exit {solution.exit_code} (failed: {sorted(solution.failed)})"
        )

    mutants = sorted((solution_dir / "mutants").glob("*.py"))
    if not mutants:
        problems.append(f"{label}: no mutants in solutions/{relative.as_posix()}/mutants")
    for mutant in mutants:
        name = mutant.stem
        caught_by = read_caught_by(mutant)
        if not caught_by:
            problems.append(f"{label}: mutant {name}: CAUGHT_BY is missing or empty")
        result = run_lesson_tests(lesson_dir, f"mutant:{name}", repo_root)
        if result.exit_code == 0:
            problems.append(f"{label}: mutant {name}: not caught (all tests passed)")
            continue
        if result.exit_code != 1:
            problems.append(
                f"{label}: mutant {name}: expected failing tests (exit 1), "
                f"got exit {result.exit_code}"
            )
        for test in caught_by:
            if not _matches(test, result.failed):
                problems.append(f"{label}: mutant {name}: {test} did not fail")

    for alternative in sorted((solution_dir / "alternatives").glob("*.py")):
        name = alternative.stem
        result = run_lesson_tests(lesson_dir, f"alternative:{name}", repo_root)
        if result.exit_code != 0:
            problems.append(
                f"{label}: alternative {name}: expected all tests to pass (exit 0), "
                f"got exit {result.exit_code} (failed: {sorted(result.failed)})"
            )

    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the lesson gate.")
    parser.add_argument("lessons", nargs="*", type=Path, help="lesson directories (default: all)")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    lessons = args.lessons or discover_lessons(args.repo_root)
    problems: list[str] = []
    for lesson in lessons:
        problems += gate_lesson(lesson, args.repo_root)
    for problem in problems:
        print(problem)
    print(f"lesson gate: {len(lessons)} lesson(s), {len(problems)} problem(s)")
    return 1 if problems else 0
