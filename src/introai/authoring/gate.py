"""The lesson gate: proof that a lesson's tests do their job.

For every lesson (a directory under ``modules/`` with a ``test_task.py``) the
same tests must:

1. reject the untouched starter ``task.py`` with ordinary test failures (pytest
   exit code 1 and no errors: the starter must import cleanly), without the
   output revealing any Part A answer from the solution;
2. accept the reference solution;
3. reject every mutant, with the tests listed in its ``CAUGHT_BY`` failing (not
   erroring);
4. accept every alternative correct implementation.

Every pytest run has a time limit, so a hanging implementation is reported
instead of blocking the gate.
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

DEFAULT_TIMEOUT = 300.0


@dataclass(frozen=True)
class PytestResult:
    exit_code: int
    failed: frozenset[str]
    passed: frozenset[str]
    errored: frozenset[str] = frozenset()
    output: str = ""
    timed_out: bool = False


def discover_lessons(repo_root: Path) -> list[Path]:
    """Lesson directories: those under ``modules/`` that contain ``test_task.py``."""
    modules = Path(repo_root) / "modules"
    if not modules.is_dir():
        return []
    return sorted(test.parent for test in modules.rglob("test_task.py"))


def _module_assignments(path: Path) -> list[tuple[str, ast.expr]]:
    tree = ast.parse(Path(path).read_bytes())
    found = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    found.append((target.id, node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value:
            found.append((node.target.id, node.value))
    return found


def read_caught_by(path: Path) -> tuple[str, ...]:
    """The ``CAUGHT_BY`` tuple of a mutant file, read without importing it."""
    for name, value in _module_assignments(path):
        if name == "CAUGHT_BY":
            return tuple(ast.literal_eval(value))
    return ()


def read_part_a_answers(path: Path) -> dict[str, list]:
    """Hand-traced answers in a solution: module-level UPPERCASE names bound to lists."""
    answers: dict[str, list] = {}
    for name, value in _module_assignments(path):
        if name == "CAUGHT_BY" or not name.isupper():
            continue
        try:
            literal = ast.literal_eval(value)
        except ValueError:
            continue
        if isinstance(literal, list | tuple) and literal:
            answers[name] = list(literal)
    return answers


def _answer_fingerprint(answer: list) -> str:
    """The start of an answer's repr, as pytest would print it (it truncates long lists)."""
    return repr(answer[:3])[:-1]


def run_lesson_tests(
    lesson_dir: Path, impl: str, repo_root: Path, timeout: float = DEFAULT_TIMEOUT
) -> PytestResult:
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
        try:
            completed = subprocess.run(
                command, cwd=repo_root, capture_output=True, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            return PytestResult(-1, frozenset(), frozenset(), timed_out=True)
        failed: set[str] = set()
        errored: set[str] = set()
        passed: set[str] = set()
        if junit.exists():
            for case in ET.parse(junit).getroot().iter("testcase"):
                name = case.get("name", "")
                if case.find("error") is not None:
                    errored.add(name)
                elif case.find("failure") is not None:
                    failed.add(name)
                elif case.find("skipped") is None:
                    passed.add(name)
    return PytestResult(
        completed.returncode,
        frozenset(failed),
        frozenset(passed),
        frozenset(errored),
        completed.stdout + completed.stderr,
    )


def _matches(test: str, names: frozenset[str]) -> bool:
    return any(name == test or name.startswith(test + "[") for name in names)


def gate_lesson(lesson_dir: Path, repo_root: Path, timeout: float = DEFAULT_TIMEOUT) -> list[str]:
    """Check one lesson; return a list of problems (empty when the lesson passes)."""
    lesson_dir = Path(lesson_dir).resolve()
    repo_root = Path(repo_root).resolve()
    relative = lesson_dir.relative_to(repo_root / "modules")
    label = f"modules/{relative.as_posix()}"
    solution_dir = repo_root / "solutions" / relative
    problems: list[str] = []

    def run(impl: str, who: str) -> PytestResult | None:
        result = run_lesson_tests(lesson_dir, impl, repo_root, timeout)
        if result.timed_out:
            problems.append(f"{label}: {who}: timed out after {timeout:g} s")
            return None
        return result

    starter = run("task", "starter")
    if starter is not None:
        if starter.exit_code != 1:
            problems.append(
                f"{label}: starter: expected failing tests (exit 1), got exit {starter.exit_code}"
            )
        if starter.errored:
            problems.append(
                f"{label}: starter: {len(starter.errored)} test(s) ended with an error instead "
                "of a failure — does the untouched task.py import cleanly?"
            )
        solution_file = solution_dir / "task.py"
        if solution_file.exists():
            for name, answer in read_part_a_answers(solution_file).items():
                if _answer_fingerprint(answer) in starter.output:
                    problems.append(
                        f"{label}: starter: the test output reveals the answer for {name}"
                    )

    solution = run("solution", "solution")
    if solution is not None and solution.exit_code != 0:
        problems.append(
            f"{label}: solution: expected all tests to pass (exit 0), "
            f"got exit {solution.exit_code} (failed: {sorted(solution.failed | solution.errored)})"
        )

    mutants = sorted((solution_dir / "mutants").glob("*.py"))
    if not mutants:
        problems.append(f"{label}: no mutants in solutions/{relative.as_posix()}/mutants")
    for mutant in mutants:
        name = mutant.stem
        caught_by = read_caught_by(mutant)
        if not caught_by:
            problems.append(f"{label}: mutant {name}: CAUGHT_BY is missing or empty")
        result = run(f"mutant:{name}", f"mutant {name}")
        if result is None:
            continue
        if result.exit_code == 0:
            problems.append(f"{label}: mutant {name}: not caught (all tests passed)")
            continue
        if result.exit_code != 1:
            problems.append(
                f"{label}: mutant {name}: expected failing tests (exit 1), "
                f"got exit {result.exit_code}"
            )
        if result.errored:
            problems.append(
                f"{label}: mutant {name}: {len(result.errored)} test(s) ended with an error "
                "instead of a failure — a mutant must import and run, and fail on its bug"
            )
        for test in caught_by:
            if not _matches(test, result.failed):
                problems.append(f"{label}: mutant {name}: {test} did not fail")

    for alternative in sorted((solution_dir / "alternatives").glob("*.py")):
        name = alternative.stem
        result = run(f"alternative:{name}", f"alternative {name}")
        if result is not None and result.exit_code != 0:
            problems.append(
                f"{label}: alternative {name}: expected all tests to pass (exit 0), "
                f"got exit {result.exit_code} (failed: {sorted(result.failed | result.errored)})"
            )

    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the lesson gate.")
    parser.add_argument("lessons", nargs="*", type=Path, help="lesson directories (default: all)")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="seconds per run")
    args = parser.parse_args(argv)

    lessons = args.lessons or discover_lessons(args.repo_root)
    problems: list[str] = []
    for lesson in lessons:
        problems += gate_lesson(lesson, args.repo_root, args.timeout)
    for problem in problems:
        print(problem)
    print(f"lesson gate: {len(lessons)} lesson(s), {len(problems)} problem(s)")
    return 1 if problems else 0
