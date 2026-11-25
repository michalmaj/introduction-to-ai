"""Self-check for lesson 1.3: formulating the parcel pickup problem.

Run from the repository root:

    uv run pytest modules/01_agents/03_problem_formulation
"""

from pathlib import Path

import pytest

from introai.search.reference import bfs
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.search import assert_valid_solution
from introai.trace import TraceLimitExceeded, record
from introai.world.reference import ParcelPickupProblem as ReferenceProblem
from introai.world.warehouse import WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
FROZENSET_HINT = (
    "cannot be put in a set, so a search cannot remember it — keep the parcels in a "
    "frozenset, not a set or a list (parcels - {cell} gives a new frozenset)"
)
PARCELS = WarehouseMap.from_file(MAPS / "parcels.txt")
A, B, C = (1, 3), (1, 5), (3, 3)


def guarded(impl, call, *args):
    """Run student code with a step budget, turning endless loops into a hint."""
    failure = None
    try:
        with step_budget(impl.__file__, 2_000_000):
            return call(*args)
    except StepBudgetExceeded:
        failure = "your problem ran for too long — is there a loop that never ends?"
    if failure:
        pytest.fail(failure, pytrace=False)


def make(impl, warehouse=PARCELS):
    return guarded(impl, impl.ParcelPickupProblem, warehouse)


# --- Part A: counting states -----------------------------------------------------------


def test_part_a_num_states(impl):
    value = impl.NUM_STATES
    if value is None:
        pytest.fail("Part A: fill in NUM_STATES in task.py", pytrace=False)
    if not isinstance(value, int):
        pytest.fail(f"Part A: NUM_STATES must be a whole number, not {value!r}", pytrace=False)
    free = sum(
        PARCELS.is_free((row, col)) for row in range(PARCELS.rows) for col in range(PARCELS.cols)
    )
    if value != free * 2 ** len(PARCELS.parcels):
        pytest.fail(
            "Part A: NUM_STATES is not right yet. A state is a robot cell together with the set "
            "of parcels still on the floor: count the possible cells and the possible sets.",
            pytrace=False,
        )


# --- Part B: the problem ---------------------------------------------------------------


def test_initial_state(impl):
    problem = make(impl)
    assert problem.initial == ((1, 1), frozenset({A, B, C})), (
        "the initial state is (the robot's start cell, the parcels on the map)"
    )


@pytest.mark.parametrize(
    "cell, parcels, expected",
    [
        ((1, 1), {A, B, C}, {"E", "S"}),
        (A, {A, C}, {"S", "W", "PICK"}),
        (A, {C}, {"S", "W"}),
        ((2, 4), {B}, {"E", "W"}),
    ],
)
def test_actions_moves_and_pick(impl, cell, parcels, expected):
    problem = make(impl)
    actions = guarded(impl, problem.actions, (cell, frozenset(parcels)))
    assert set(actions) == expected, (
        f"in state ({cell}, {sorted(parcels)}) the possible actions are {sorted(expected)}: moves "
        "into free cells, and PICK only when a parcel lies on the robot's cell"
    )
    assert len(actions) == len(set(actions)), "list every action once"


def test_result_move(impl):
    problem = make(impl)
    state = ((1, 1), frozenset({A}))
    assert guarded(impl, problem.result, state, "E") == ((1, 2), frozenset({A})), (
        "a move changes only the robot's cell"
    )


def test_result_pick_removes_parcel(impl):
    problem = make(impl)
    after = guarded(impl, problem.result, (A, frozenset({A, C})), "PICK")
    assert after == (A, frozenset({C})), "PICK removes the parcel from the robot's cell"
    if not isinstance(after[1], frozenset):
        pytest.fail(
            f"after PICK the parcels are a {type(after[1]).__name__}: {FROZENSET_HINT}",
            pytrace=False,
        )


def test_result_does_not_change_its_input(impl):
    problem = make(impl)
    state = problem.initial
    for action in ("E", "E"):
        state = guarded(impl, problem.result, state, action)
    snapshot = (state[0], set(state[1]))
    guarded(impl, problem.result, state, "PICK")
    assert (state[0], set(state[1])) == snapshot, (
        "result must return a new state and leave the old one unchanged"
    )


def test_states_are_hashable(impl):
    problem = make(impl)
    states = [problem.initial]
    for action in ("E", "E", "PICK"):  # a move, another move, then a pick on the parcel (1, 3)
        states.append(guarded(impl, problem.result, states[-1], action))
    for state in states:
        try:
            hash(state)
        except TypeError:
            pytest.fail(f"the state {state!r} {FROZENSET_HINT}", pytrace=False)


def test_is_goal(impl):
    problem = make(impl)
    assert guarded(impl, problem.is_goal, ((2, 4), frozenset())), (
        "with no parcels left the goal is reached, wherever the robot stands"
    )
    assert not guarded(impl, problem.is_goal, (PARCELS.dock, frozenset({A}))), (
        "the dock is not the goal: the goal is to collect every parcel"
    )


@pytest.mark.parametrize("parcels", [[A], [A, C], [A, B, C]], ids=["1", "2", "3"])
def test_bfs_finds_optimal_plan(impl, parcels):
    warehouse = PARCELS.with_parcels(parcels)
    problem = make(impl, warehouse)
    failure = None
    try:
        with record(limit=200_000, kinds={"expand"}), step_budget(impl.__file__, 5_000_000):
            node = bfs(problem)
    except (TraceLimitExceeded, StepBudgetExceeded):
        failure = "breadth-first search on your problem did not finish — check actions and result"
    except TypeError as error:
        if "unhashable" not in str(error):
            raise
        failure = f"a state of your problem {FROZENSET_HINT}"
    if failure:
        pytest.fail(failure, pytrace=False)
    if node is None:
        pytest.fail("breadth-first search found no plan, but one exists", pytrace=False)
    assert_valid_solution(problem, node)
    optimal = len(bfs(ReferenceProblem(warehouse)).solution())
    assert len(node.solution()) == optimal, (
        f"the plan has {len(node.solution())} actions, the shortest has {optimal}"
    )


def test_task_does_not_import_reference(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, f"task.py imports {found}: write the problem yourself"
