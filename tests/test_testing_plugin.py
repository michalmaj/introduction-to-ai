import subprocess
import sys


def run_pytest(cwd, args):
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_plugin_runs_from_root_and_from_lesson_dir(fake_repo):
    lesson = fake_repo / "modules" / "99_fake" / "01_add"
    assert run_pytest(fake_repo, [str(lesson)]).returncode == 1
    assert run_pytest(fake_repo, [str(lesson), "--impl=solution"]).returncode == 0
    assert run_pytest(lesson, []).returncode == 1
    assert run_pytest(lesson, ["--impl=solution"]).returncode == 0


def test_plugin_loads_mutants_and_alternatives(fake_repo):
    lesson = fake_repo / "modules" / "99_fake" / "01_add"
    assert run_pytest(fake_repo, [str(lesson), "--impl=mutant:off_by_one"]).returncode == 1
    assert run_pytest(fake_repo, [str(lesson), "--impl=alternative:sum_list"]).returncode == 0


def test_plugin_reports_bad_impl_value(fake_repo):
    lesson = fake_repo / "modules" / "99_fake" / "01_add"
    result = run_pytest(fake_repo, [str(lesson), "--impl=nonsense"])
    assert result.returncode != 0
    assert "unknown --impl value 'nonsense'" in result.stdout + result.stderr


def test_bare_pytest_from_root_hints_how_to_check_a_lesson(fake_repo):
    root_run = run_pytest(fake_repo, [])
    assert root_run.returncode == 0
    assert "uv run pytest modules/<module>/<lesson>" in root_run.stdout
    lesson = fake_repo / "modules" / "99_fake" / "01_add"
    lesson_run = run_pytest(fake_repo, [str(lesson), "--impl=solution"])
    assert "uv run pytest modules/<module>/<lesson>" not in lesson_run.stdout
