"""Regression guards for lesson 2.2's tests: they must not leak answers or hang."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from introai.authoring.gate import read_part_a_answers

REPO = Path(__file__).resolve().parents[1]
LESSON = REPO / "modules" / "02_search" / "02_bfs_dfs"
SOLUTION = REPO / "solutions" / "02_search" / "02_bfs_dfs" / "task.py"


def copy_lesson(root: Path, task_source: str) -> Path:
    """A minimal repository holding lesson 2.2's tests and the given task.py."""
    lesson = root / "modules" / "02_search" / "02_bfs_dfs"
    lesson.mkdir(parents=True)
    shutil.copy(LESSON / "test_task.py", lesson / "test_task.py")
    (lesson / "task.py").write_text(task_source)
    shutil.copytree(REPO / "data", root / "data")
    (root / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\naddopts = ["--import-mode=importlib"]\n'
    )
    (root / "conftest.py").write_text('pytest_plugins = ["introai.testing.plugin"]\n')
    return lesson


@pytest.mark.parametrize("variant", ["starter", "wrong_answer"])
def test_part_a_answers_never_appear_in_test_output(tmp_path, variant):
    solution = SOLUTION.read_text()
    if variant == "starter":
        source = (LESSON / "task.py").read_text()
    else:
        source = solution.replace(
            'BFS_PATH: list[str] | None = ["A", "C", "F", "H"]',
            'BFS_PATH: list[str] | None = ["A", "B", "D", "H"]',
        )
        assert source != solution
    lesson = copy_lesson(tmp_path, source)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(lesson), "-l", "-p", "no:cacheprovider"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 1
    output = result.stdout + result.stderr
    for name, answer in read_part_a_answers(SOLUTION).items():
        assert repr(answer[:3])[:-1] not in output, f"the output reveals {name}"


PEEKING_DFS = """
from introai.search import Node, expand


def dfs(problem):
    frontier = [Node(problem.initial)]
    expanded = set()
    while frontier:
        node = frontier[-1]  # BUG: peeks instead of removing the node
        if node.state in expanded:
            continue
        if problem.is_goal(node.state):
            return node
        expanded.add(node.state)
        for child in reversed(expand(problem, node)):
            if child.state not in expanded:
                frontier.append(child)
    return None
"""

GUARD_SCRIPT = """
import sys

import pytest

from introai.search.examples import exercise
from introai.testing.impl import load_module

lesson_tests = load_module(sys.argv[1])
buggy = load_module(sys.argv[2])
try:
    lesson_tests.search(buggy.dfs, exercise())
except pytest.fail.Exception as failure:
    print("FAILED:", failure)
    sys.exit(0)
print("RETURNED")
sys.exit(1)
"""


def test_endless_loop_without_expand_fails_fast(tmp_path):
    buggy = tmp_path / "peeking.py"
    buggy.write_text(PEEKING_DFS)
    script = tmp_path / "guard.py"
    script.write_text(GUARD_SCRIPT)
    result = subprocess.run(
        [sys.executable, str(script), str(LESSON / "test_task.py"), str(buggy)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ran for too long" in result.stdout
