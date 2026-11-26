"""Self-check for lesson 2.3: uniform-cost search.

Run from the repository root:

    uv run pytest modules/02_search/03_uniform_cost_search

The tests check properties every correct implementation has (valid paths, the
cheapest cost, expansions in order of non-decreasing path cost), not one
particular way of writing the code. The lesson's "What the tests do not check"
section lists what is left for you to judge.
"""

from pathlib import Path

import pytest

from introai.search.examples import (
    cyclic,
    disconnected,
    weighted_example,
    weighted_exercise,
    worked_example,
)
from introai.search.problems import GraphProblem
from introai.search.reference import ucs as reference_ucs
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.search import assert_valid_solution, expanded_nodes, first_decrease
from introai.trace import TraceLimitExceeded, record
from introai.world.warehouse import RouteProblem, WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
LIMIT = 10_000  # expansions
STEP_BUDGET = 500_000  # lines executed in task.py during one search

PROBLEMS = {
    "weighted_example": weighted_example,
    "weighted_exercise": weighted_exercise,
    "unit_costs": worked_example,
    "congested_map": lambda: RouteProblem(WarehouseMap.from_file(MAPS / "congested.txt")),
    "aisles_map": lambda: RouteProblem(WarehouseMap.from_file(MAPS / "aisles.txt")),
}
TIE_HINT = (
    "Python compared two Node objects, which it cannot do: when two entries in the heap "
    "have the same cost, heapq compares the next item of the tuples. Put a counter between "
    "the cost and the node, for example (cost, next(counter), node)"
)


def search(impl, problem, limit=LIMIT, hint=""):
    """Run ucs, recording its expansions; turn endless loops into quick failures."""
    failure = None
    try:
        with record(limit=limit) as trace, step_budget(impl.__file__, STEP_BUDGET):
            result = impl.ucs(problem)
    except (TraceLimitExceeded, RecursionError):
        failure = (
            f"ucs made more than {limit} expansions {hint}— do you keep track of the states "
            "you have already reached, with the cheapest cost found so far?"
        )
    except StepBudgetExceeded:
        failure = (
            "ucs ran for too long without finishing — is there a loop that never ends, for "
            "example one that looks at the frontier without removing a node?"
        )
    except TypeError as error:
        if "not supported between instances" not in str(error):
            raise
        failure = TIE_HINT
    if failure:
        pytest.fail(failure, pytrace=False)
    return result, expanded_nodes(trace)


# --- Part A: hand-traced answers -------------------------------------------------------


def reference_answer():
    with record() as trace:
        node = reference_ucs(weighted_exercise())
    return [n.state for n in expanded_nodes(trace)], node.states()


def check_part_a(value, expected, name):
    # pytrace=False: no traceback at all, so pytest cannot print `expected` as a frame
    # argument or local variable. The message must never reveal the answer.
    if value is None:
        pytest.fail(f"Part A: fill in {name} in task.py", pytrace=False)
    if not isinstance(value, list | tuple):
        pytest.fail(
            f"Part A: {name} must be a list of state names, "
            f'for example ["A", "B"], not {type(value).__name__}',
            pytrace=False,
        )
    if list(value) != expected:
        pytest.fail(
            f"Part A: {name} is not right yet (the correct list has {len(expected)} states). "
            "Trace the exercise graph again, following the rules in the lesson.",
            pytrace=False,
        )


def test_part_a_ucs_expansion_order(impl):
    check_part_a(impl.UCS_EXPANSION_ORDER, reference_answer()[0], "UCS_EXPANSION_ORDER")


def test_part_a_ucs_path(impl):
    check_part_a(impl.UCS_PATH, reference_answer()[1], "UCS_PATH")


# --- Part B: uniform-cost search -------------------------------------------------------


def test_ucs_returns_root_when_start_is_goal(impl):
    problem = GraphProblem.undirected_weighted([("A", "B", 1)], "A", "A")
    result, _ = search(impl, problem)
    if result is None:
        pytest.fail("ucs returned None, but the start state is already the goal", pytrace=False)
    assert_valid_solution(problem, result)
    assert result.states() == ["A"], "the start state is the goal: return the root node"


@pytest.mark.parametrize("name", PROBLEMS)
def test_ucs_finds_the_cheapest_path(impl, name):
    problem = PROBLEMS[name]()
    result, _ = search(impl, problem)
    if result is None:
        pytest.fail(f"ucs returned None on {name}, but a path to the goal exists", pytrace=False)
    assert_valid_solution(problem, result)
    cheapest = reference_ucs(PROBLEMS[name]()).path_cost
    if result.path_cost > cheapest + 1e-9:
        # The cheapest cost is not printed: on the exercise graph it would be a hint.
        pytest.fail(
            f"ucs found a path of cost {result.path_cost:g} on {name}, but a cheaper one "
            "exists. Do you test for the goal when a node is removed from the frontier, and "
            "do you add a child again when you find a cheaper path to its state?",
            pytrace=False,
        )


@pytest.mark.parametrize("name", ["weighted_example", "congested_map"])
def test_ucs_expands_in_nondecreasing_path_cost(impl, name):
    _, nodes = search(impl, PROBLEMS[name]())
    violation = first_decrease(nodes, key=lambda node: node.path_cost)
    if violation:
        _, before, after = violation
        pytest.fail(
            f"on {name} ucs expanded {after.state} (path cost {after.path_cost:g}) right after "
            f"{before.state} (path cost {before.path_cost:g}). UCS always expands the cheapest "
            "node in the frontier — is the frontier a priority queue ordered by path cost?",
            pytrace=False,
        )


def test_ucs_breaks_ties_between_equal_costs(impl):
    problem = worked_example()  # every step costs 1, so many nodes have the same cost
    result, _ = search(impl, problem)
    if result is None:
        pytest.fail("ucs returned None, but a path to the goal exists", pytrace=False)
    assert_valid_solution(problem, result)


def test_ucs_terminates_on_a_graph_with_cycles(impl):
    result, nodes = search(impl, cyclic(), limit=1000, hint="on a 4-state graph ")
    assert result is None, "this graph has no goal, so ucs must return None"
    assert {node.state for node in nodes} == {"A", "B", "C", "D"}, (
        "with no goal ucs must expand every reachable state before it gives up"
    )


def test_ucs_returns_none_when_goal_unreachable(impl):
    result, _ = search(impl, disconnected())
    assert result is None, "the goal cannot be reached from the start, so ucs must return None"


def test_ucs_uses_expand(impl):
    _, nodes = search(impl, weighted_example())
    if not nodes:
        pytest.fail(
            "ucs expanded no nodes that the tests could see — use expand(problem, node) "
            "from introai.search to generate children",
            pytrace=False,
        )


def test_task_does_not_import_reference_search(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, (
        f"task.py imports {found}: write the algorithm yourself instead of importing the "
        "course's reference version"
    )
