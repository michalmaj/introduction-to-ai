"""Self-check for lesson 2.7: designing heuristics.

Run from the repository root:

    uv run pytest modules/02_search/07_designing_heuristics

Your heuristic is checked against the exact cost of every state reachable on
three small maps, so a test failure shows a concrete state where it goes wrong.
That is strong evidence, but not a proof for every possible map: the argument
for admissibility is still yours to make.
"""

from pathlib import Path

import pytest

from introai.search.reference import a_star
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.search import first_inadmissible
from introai.trace import record
from introai.world.reference import CANDIDATE_ADMISSIBLE, ParcelPickupProblem
from introai.world.warehouse import WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
AISLES = WarehouseMap.from_file(MAPS / "aisles.txt")
CELLS = [(3, 1), (5, 4), (9, 21), (13, 15)]
WAREHOUSES = {
    "parcels": WarehouseMap.from_file(MAPS / "parcels.txt"),
    "aisles2": AISLES.with_parcels(CELLS[:2]),
    "aisles3": AISLES.with_parcels(CELLS[:3]),
    "aisles4": AISLES.with_parcels(CELLS[:4]),
}
STEP_BUDGET = 3_000_000  # lines executed in task.py during one test


def describe(state):
    cell, parcels = state
    return f"robot at {cell}, parcels left {sorted(parcels) if parcels else 'none'}"


def checked(impl):
    """Your heuristic, wrapped so that crashes and odd values become clear hints."""

    def h(state):
        failure = None
        try:
            value = impl.parcel_heuristic(state)
        except StepBudgetExceeded:
            raise
        except Exception as error:  # the student's code may raise anything
            failure = (
                f"parcel_heuristic crashed at the state ({describe(state)}) with "
                f"{type(error).__name__}: {error}"
            )
            if not state[1]:
                failure += " — with no parcels left, return 0"
        else:
            if isinstance(value, bool) or not isinstance(value, int | float):
                failure = f"parcel_heuristic must return a number, not {value!r}"
            elif value < 0:
                failure = (
                    f"parcel_heuristic returned {value} at ({describe(state)}): a cost "
                    "estimate is never negative"
                )
        if failure:
            pytest.fail(failure, pytrace=False)
        return value

    return h


def guarded(impl, call, *args):
    try:
        with step_budget(impl.__file__, STEP_BUDGET):
            return call(*args)
    except StepBudgetExceeded:
        pytest.fail(
            "parcel_heuristic is too slow or loops forever — it is called thousands of times",
            pytrace=False,
        )


def expansions(problem, h):
    with record(kinds={"expand"}) as trace:
        node = a_star(problem, h)
    return node, len(trace.of_kind("expand"))


# --- Part A: which candidates are admissible -------------------------------------------


def test_part_a_admissible(impl):
    # pytrace=False: no traceback, so pytest cannot print the expected answers.
    value = impl.ADMISSIBLE
    if not isinstance(value, dict) or set(value) != set(CANDIDATE_ADMISSIBLE):
        pytest.fail("Part A: ADMISSIBLE must keep the keys h1, ..., h6 from task.py", pytrace=False)
    empty = sorted(name for name, answer in value.items() if answer is None)
    if empty:
        pytest.fail(f"Part A: fill in ADMISSIBLE for {', '.join(empty)}", pytrace=False)
    if not all(isinstance(answer, bool) for answer in value.values()):
        pytest.fail("Part A: write True or False for each heuristic", pytrace=False)
    wrong = sum(value[name] != CANDIDATE_ADMISSIBLE[name] for name in CANDIDATE_ADMISSIBLE)
    if wrong:
        answers = "answer is" if wrong == 1 else "answers are"
        pytest.fail(
            f"Part A: {wrong} of the 6 {answers} not right yet. For each heuristic, look for "
            "a state where it would promise more than the robot really has to do.",
            pytrace=False,
        )


# --- Part B: your heuristic ------------------------------------------------------------


def test_heuristic_is_zero_at_goal_states(impl):
    h = checked(impl)
    for cell in [(1, 1), (1, 3), (3, 5)]:
        value = guarded(impl, h, (cell, frozenset()))
        assert value == 0, (
            f"with no parcels left ({describe((cell, frozenset()))}) the goal is reached and "
            f"the true cost is 0, so an admissible heuristic must give 0, not {value}"
        )


@pytest.mark.parametrize("name", ["parcels", "aisles2", "aisles3"])
def test_heuristic_is_admissible(impl, name):
    problem = ParcelPickupProblem(WAREHOUSES[name])
    found = guarded(impl, first_inadmissible, problem, checked(impl))
    if found:
        state, value, true = found
        pytest.fail(
            f"on {name} your heuristic gives {value:g} at the state ({describe(state)}), but "
            f"the robot can collect everything from there for {true:g}: it overestimates",
            pytrace=False,
        )


@pytest.mark.parametrize("name", ["parcels", "aisles3"])
def test_a_star_with_your_heuristic_finds_the_cheapest_plan(impl, name):
    problem = ParcelPickupProblem(WAREHOUSES[name])
    node, _ = guarded(impl, expansions, problem, checked(impl))
    best, _ = expansions(ParcelPickupProblem(WAREHOUSES[name]), lambda state: 0)
    assert node.path_cost == best.path_cost, (
        f"A* with your heuristic found a plan of {node.path_cost:g} actions on {name}, but "
        f"{best.path_cost:g} is enough — the heuristic must not overestimate"
    )


@pytest.mark.parametrize("name", ["aisles3", "aisles4"])
def test_heuristic_beats_counting_parcels(impl, name):
    problem = ParcelPickupProblem(WAREHOUSES[name])
    _, yours = guarded(impl, expansions, problem, checked(impl))
    _, counting = expansions(ParcelPickupProblem(WAREHOUSES[name]), lambda state: len(state[1]))
    assert yours < counting, (
        f'on {name} A* with your heuristic expanded {yours} nodes, with "number of parcels '
        f'left" {counting}: use the distances the robot has to drive, not only the picks'
    )


def test_task_does_not_import_reference(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, f"task.py imports {found}: write the heuristic yourself"
