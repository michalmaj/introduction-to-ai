import sys

import pytest

from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.impl import load_module


def test_budget_stops_an_endless_loop_in_the_target_file(tmp_path):
    path = tmp_path / "loop.py"
    path.write_text("def spin():\n    while True:\n        pass\n")
    module = load_module(path)
    with pytest.raises(StepBudgetExceeded):
        with step_budget(module.spin.__code__.co_filename, max_lines=10_000):
            module.spin()


def test_budget_ignores_other_files(tmp_path):
    path = tmp_path / "target.py"
    path.write_text("def noop():\n    return 1\n")
    module = load_module(path)
    with step_budget(module.noop.__code__.co_filename, max_lines=5):
        total = sum(range(10_000))  # many lines elsewhere, none in target.py
        assert module.noop() == 1
    assert total == 49_995_000


def test_budget_restores_the_previous_tracer(tmp_path):
    before = sys.gettrace()
    with step_budget(str(tmp_path / "none.py"), max_lines=1):
        pass
    assert sys.gettrace() is before
