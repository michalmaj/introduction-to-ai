"""Self-check for lesson 2.5: comparing search strategies.

Run from the repository root:

    uv run pytest modules/02_search/05_comparing_strategies

The tests check the table of properties in Part A. To keep you thinking, a wrong
row only reports how many of its five answers are wrong, not which ones.
"""

import pytest

from introai.search.reference import STRATEGY_PROPERTIES

ALGORITHMS = list(STRATEGY_PROPERTIES)
PROPERTY_NAMES = list(STRATEGY_PROPERTIES["BFS"])


def check_row(impl, name):
    # pytrace=False: no traceback, so pytest cannot print the expected table.
    table = impl.PROPERTIES
    if not isinstance(table, dict):
        pytest.fail("Part A: PROPERTIES must stay a dictionary, as in task.py", pytrace=False)
    missing = [
        f"{algorithm}/{name}"
        for algorithm in ALGORITHMS
        if not isinstance(table.get(algorithm), dict) or name not in table[algorithm]
    ]
    if missing:
        pytest.fail(
            f"Part A: PROPERTIES has no entry for {', '.join(missing)} — keep every key "
            "from task.py",
            pytrace=False,
        )
    values = {algorithm: table[algorithm][name] for algorithm in ALGORITHMS}
    empty = [algorithm for algorithm, value in values.items() if value is None]
    if empty:
        pytest.fail(f"Part A: fill in {name} for {', '.join(empty)} in task.py", pytrace=False)
    not_bool = {a: v for a, v in values.items() if not isinstance(v, bool)}
    if not_bool:
        algorithm, value = next(iter(not_bool.items()))
        pytest.fail(
            f"Part A: write True or False, not {value!r} ({algorithm}/{name})", pytrace=False
        )
    wrong = sum(values[a] != STRATEGY_PROPERTIES[a][name] for a in ALGORITHMS)
    if wrong:
        answers = "answer is" if wrong == 1 else "answers are"
        pytest.fail(
            f"Part A: {wrong} of the 5 {answers} for {name} not right yet. Check the exact "
            'assumptions in the lesson, section "Properties to compare".',
            pytrace=False,
        )


def test_part_a_complete_finite(impl):
    check_row(impl, "complete_finite")


def test_part_a_complete_infinite(impl):
    check_row(impl, "complete_infinite")


def test_part_a_optimal_unit_costs(impl):
    check_row(impl, "optimal_unit_costs")


def test_part_a_optimal_any_costs(impl):
    check_row(impl, "optimal_any_costs")
