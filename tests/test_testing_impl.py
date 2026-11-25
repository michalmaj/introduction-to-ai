import re

import pytest

from introai.testing.impl import load_module, resolve_impl_path


@pytest.fixture
def lesson(tmp_path):
    lesson_dir = tmp_path / "modules" / "02_x" / "01_y"
    lesson_dir.mkdir(parents=True)
    (lesson_dir / "task.py").write_text("")
    solution_dir = tmp_path / "solutions" / "02_x" / "01_y"
    (solution_dir / "mutants").mkdir(parents=True)
    (solution_dir / "alternatives").mkdir(parents=True)
    (solution_dir / "task.py").write_text("")
    (solution_dir / "mutants" / "bug.py").write_text("")
    (solution_dir / "alternatives" / "other.py").write_text("")
    return lesson_dir


@pytest.mark.parametrize(
    "impl, relative",
    [
        ("task", "modules/02_x/01_y/task.py"),
        ("solution", "solutions/02_x/01_y/task.py"),
        ("mutant:bug", "solutions/02_x/01_y/mutants/bug.py"),
        ("alternative:other", "solutions/02_x/01_y/alternatives/other.py"),
    ],
)
def test_resolve_impl_path(lesson, tmp_path, impl, relative):
    assert resolve_impl_path(lesson, impl, tmp_path) == tmp_path / relative


@pytest.mark.parametrize("impl", ["foo", "mutant:", "alternative:", "solutions"])
def test_unknown_impl_value(lesson, tmp_path, impl):
    message = (
        f"unknown --impl value {impl!r}; expected task, solution, "
        "mutant:<name> or alternative:<name>"
    )
    with pytest.raises(ValueError, match=re.escape(message)):
        resolve_impl_path(lesson, impl, tmp_path)


def test_missing_impl_file(lesson, tmp_path):
    with pytest.raises(FileNotFoundError, match="missing.py"):
        resolve_impl_path(lesson, "mutant:missing", tmp_path)


def test_load_module_keeps_same_named_files_apart(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    (tmp_path / "a" / "task.py").write_text("VALUE = 1\n")
    (tmp_path / "b" / "task.py").write_text("VALUE = 2\n")
    first = load_module(tmp_path / "a" / "task.py")
    second = load_module(tmp_path / "b" / "task.py")
    assert (first.VALUE, second.VALUE) == (1, 2)
    assert first.__name__ != second.__name__
