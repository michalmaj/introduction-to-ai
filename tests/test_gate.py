import shutil

from introai.authoring.gate import (
    discover_lessons,
    gate_lesson,
    main,
    read_caught_by,
    run_lesson_tests,
)

LESSON = "modules/99_fake/01_add"
SOLUTION = "solutions/99_fake/01_add"


def test_discover_lessons(fake_repo):
    assert discover_lessons(fake_repo) == [fake_repo / LESSON]


def test_read_caught_by(fake_repo):
    path = fake_repo / SOLUTION / "mutants" / "off_by_one.py"
    assert read_caught_by(path) == ("test_add", "test_add_negative")
    assert read_caught_by(fake_repo / SOLUTION / "task.py") == ()


def test_run_lesson_tests_reports_failed_names(fake_repo):
    result = run_lesson_tests(fake_repo / LESSON, "mutant:abs_bug", fake_repo)
    assert result.exit_code == 1
    assert result.failed == {"test_add_negative"}
    assert result.passed == {"test_add"}


def test_clean_lesson_passes_gate(fake_repo):
    assert gate_lesson(fake_repo / LESSON, fake_repo) == []


def test_uncaught_mutant_is_reported(fake_repo):
    (fake_repo / SOLUTION / "mutants" / "abs_bug.py").write_text(
        'CAUGHT_BY = ("test_add_negative",)\n\n\ndef add(a, b):\n    return a + b\n'
    )
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("mutant abs_bug" in p and "not caught" in p for p in problems)


def test_mutant_caught_by_wrong_test_is_reported(fake_repo):
    (fake_repo / SOLUTION / "mutants" / "abs_bug.py").write_text(
        'CAUGHT_BY = ("test_add",)\n\n\ndef add(a, b):\n    return abs(a) + abs(b)\n'
    )
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("mutant abs_bug" in p and "test_add did not fail" in p for p in problems)


def test_mutant_without_caught_by_is_reported(fake_repo):
    (fake_repo / SOLUTION / "mutants" / "abs_bug.py").write_text(
        "def add(a, b):\n    return abs(a) + abs(b)\n"
    )
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("mutant abs_bug" in p and "CAUGHT_BY" in p for p in problems)


def test_passing_starter_is_reported(fake_repo):
    (fake_repo / LESSON / "task.py").write_text("def add(a, b):\n    return a + b\n")
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("starter" in p for p in problems)


def test_failing_solution_is_reported(fake_repo):
    (fake_repo / SOLUTION / "task.py").write_text("def add(a, b):\n    return 0\n")
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("solution" in p for p in problems)


def test_failing_alternative_is_reported(fake_repo):
    (fake_repo / SOLUTION / "alternatives" / "sum_list.py").write_text(
        "def add(a, b):\n    return a - b\n"
    )
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("alternative sum_list" in p for p in problems)


def test_missing_mutants_are_reported(fake_repo):
    shutil.rmtree(fake_repo / SOLUTION / "mutants")
    problems = gate_lesson(fake_repo / LESSON, fake_repo)
    assert any("no mutants" in p for p in problems)


def test_main_without_lessons_succeeds(tmp_path, capsys):
    assert main(["--repo-root", str(tmp_path)]) == 0


def test_main_reports_problems(fake_repo, capsys):
    (fake_repo / LESSON / "task.py").write_text("def add(a, b):\n    return a + b\n")
    assert main(["--repo-root", str(fake_repo)]) == 1
    assert "starter" in capsys.readouterr().out
