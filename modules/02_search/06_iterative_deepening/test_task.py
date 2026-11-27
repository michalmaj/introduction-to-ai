"""Self-check for lesson 2.6: depth-limited search and iterative deepening.

Run from the repository root:

    uv run pytest modules/02_search/06_iterative_deepening

The tests check what every correct implementation does (results, cutoffs, the
depth limit, cycle checks, shortest paths, the number of repeated expansions),
not one particular way of writing the code: a recursive version passes too.
"""

from pathlib import Path

import pytest

from introai.search import CUTOFF
from introai.search.examples import (
    binary_tree,
    complete_tree,
    cyclic,
    disconnected,
    exercise,
    worked_example,
)
from introai.search.problems import GraphProblem
from introai.search.reference import bfs as reference_bfs
from introai.search.reference import depth_limited_search as reference_dls
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.search import assert_valid_solution, expanded_nodes
from introai.trace import TraceLimitExceeded, record
from introai.world.warehouse import RouteProblem, WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
LIMIT = 20_000  # expansions
STEP_BUDGET = 1_000_000  # lines executed in task.py during one call

PROBLEMS = {
    "worked_example": worked_example,
    "exercise": exercise,
    "small_map": lambda: RouteProblem(WarehouseMap.from_file(MAPS / "small.txt")),
}


def run(impl, name, *args, budget=LIMIT, hint=""):
    """Call impl.<name>(*args), recording its expansions; turn endless runs into hints."""
    failure = None
    try:
        with record(limit=budget) as trace, step_budget(impl.__file__, STEP_BUDGET):
            result = getattr(impl, name)(*args)
    except TraceLimitExceeded:
        failure = (
            f"{name} made more than {budget} expansions {hint}— does depth-limited search "
            "stop at the limit and skip states that are already on the current path?"
        )
    except RecursionError:
        failure = f"{name} recursed too deeply — does every recursive call lower the limit?"
    except StepBudgetExceeded:
        failure = f"{name} ran for too long — is there a loop that never ends?"
    if failure:
        pytest.fail(failure, pytrace=False)
    return result, expanded_nodes(trace)


def dls(impl, problem, limit, **kwargs):
    return run(impl, "depth_limited_search", problem, limit, **kwargs)


def ids(impl, problem, **kwargs):
    return run(impl, "iterative_deepening_search", problem, **kwargs)


# --- Part A: counting expansions by hand ----------------------------------------------


def reference_expansions_per_iteration(problem):
    counts, limit = [], 0
    while True:
        with record(kinds={"expand"}) as trace:
            result = reference_dls(problem, limit)
        counts.append(len(trace.of_kind("expand")))
        if result is not CUTOFF:
            return counts
        limit += 1


def test_part_a_ids_expansions_per_iteration(impl):
    # pytrace=False: no traceback, so pytest cannot print `expected`. Never reveal it.
    value, name = impl.IDS_EXPANSIONS_PER_ITERATION, "IDS_EXPANSIONS_PER_ITERATION"
    expected = reference_expansions_per_iteration(exercise())
    if value is None:
        pytest.fail(f"Part A: fill in {name} in task.py", pytrace=False)
    if not isinstance(value, list | tuple) or not all(
        isinstance(v, int) and not isinstance(v, bool) for v in value
    ):
        pytest.fail(
            f"Part A: {name} must be a list of whole numbers, for example [0, 1, 2]",
            pytrace=False,
        )
    if list(value) != expected:
        pytest.fail(
            f"Part A: {name} is not right yet (the correct list has {len(expected)} "
            "numbers, one per depth limit). Trace the exercise graph again, following the "
            "rules in the lesson.",
            pytrace=False,
        )


# --- Part B: depth-limited search ------------------------------------------------------


def test_dls_returns_root_when_start_is_goal(impl):
    problem = GraphProblem.undirected([("A", "B")], "A", "A")
    result, _ = dls(impl, problem, 0)
    if result is None or result == CUTOFF:
        pytest.fail(
            "the start state is the goal: depth_limited_search must return the root, even "
            "with limit 0",
            pytrace=False,
        )
    assert result.states() == ["A"], "the start state is the goal: return the root node"


def test_dls_finds_a_goal_within_the_limit(impl):
    problem = worked_example()
    result, _ = dls(impl, problem, 3)
    if result is None or result == CUTOFF:
        pytest.fail(
            f"depth_limited_search(worked_example, 3) returned {result!r}, but the goal G "
            "lies at depth 3",
            pytrace=False,
        )
    assert_valid_solution(problem, result)
    assert result.depth <= 3, f"the returned path has {result.depth} steps, more than the limit"


def test_dls_reports_cutoff(impl):
    result, _ = dls(impl, worked_example(), 2)
    if result != CUTOFF:
        pytest.fail(
            f"depth_limited_search(worked_example, 2) returned {result!r}. The goal lies "
            "deeper than the limit, so the search was cut off: return CUTOFF (from "
            "introai.search), so that iterative deepening knows it must go deeper",
            pytrace=False,
        )


@pytest.mark.parametrize(
    "make, limit",
    [(binary_tree, 4), (disconnected, 5)],
    ids=["binary_tree", "disconnected"],
)
def test_dls_returns_none_when_nothing_was_cut(impl, make, limit):
    result, _ = dls(impl, make(), limit)
    assert result is None, (
        f"with limit {limit} nothing was cut off and no goal was found, so the answer is "
        f"None (there is no goal at all), not {result!r}"
    )


def test_dls_respects_the_limit(impl):
    _, nodes = dls(impl, binary_tree(), 2)
    too_deep = [node for node in nodes if node.depth >= 2]
    assert not too_deep, (
        f"with limit 2 depth_limited_search expanded {too_deep[0].state} at depth "
        f"{too_deep[0].depth}: a node at the limit is cut off, not expanded"
    )


def test_dls_skips_cycles(impl):
    _, nodes = dls(impl, cyclic(), 6, budget=5000, hint="on a 4-state graph ")
    for node in nodes:
        if node.state in node.states()[:-1]:
            pytest.fail(
                f"depth_limited_search expanded {node.state} on the path {node.states()}: "
                "the state is already on the path, so this is a cycle — do not expand it",
                pytrace=False,
            )


# --- Part B: iterative deepening -------------------------------------------------------


def test_ids_returns_root_when_start_is_goal(impl):
    problem = GraphProblem.undirected([("A", "B")], "A", "A")
    result, _ = ids(impl, problem)
    if result is None or result == CUTOFF:
        pytest.fail("the start state is the goal: return the root node", pytrace=False)
    assert result.states() == ["A"], "the start state is the goal: return the root node"


@pytest.mark.parametrize("name", PROBLEMS)
def test_ids_finds_a_shortest_path(impl, name):
    problem = PROBLEMS[name]()
    result, _ = ids(impl, problem)
    if result is None or result == CUTOFF:
        pytest.fail(
            f"iterative_deepening_search returned {result!r} on {name}, but a path to the "
            "goal exists — does it try the next limit whenever the search was cut off?",
            pytrace=False,
        )
    assert_valid_solution(problem, result)
    shortest = len(reference_bfs(PROBLEMS[name]()).solution())
    assert len(result.solution()) == shortest, (
        f"iterative deepening found a {len(result.solution())}-step path on {name}; the "
        f"shortest has {shortest} — do you try the limits 0, 1, 2, ... in order?"
    )


def test_ids_terminates_on_a_graph_with_cycles(impl):
    result, _ = ids(impl, cyclic(), budget=1000, hint="on a 4-state graph ")
    assert result is None, "this graph has no goal, so iterative deepening must return None"


def test_ids_returns_none_when_goal_unreachable(impl):
    result, _ = ids(impl, disconnected())
    assert result is None, "the goal cannot be reached, so iterative deepening must return None"


def test_ids_expansions_match_the_theory(impl):
    # A full binary tree of depth 4 with the goal in the last leaf that DFS reaches.
    tree = GraphProblem(complete_tree(2, 4).adjacency, "r", "r1111")
    result, nodes = ids(impl, tree)
    if result is None or result == CUTOFF:
        pytest.fail(
            "iterative deepening did not find the goal of a full binary tree", pytrace=False
        )
    expected = sum(2**limit - 1 for limit in range(5))
    assert len(nodes) == expected, (
        f"on a full binary tree of depth 4, with the goal in the last leaf, iterative "
        f"deepening should expand {expected} nodes in total (every round expands all the "
        f"nodes above its limit). Yours expanded {len(nodes)}"
    )


# --- Both functions --------------------------------------------------------------------


@pytest.mark.parametrize("name", ["depth_limited_search", "iterative_deepening_search"])
def test_task_uses_expand(impl, name):
    args = (worked_example(), 3) if name == "depth_limited_search" else (worked_example(),)
    _, nodes = run(impl, name, *args)
    if not nodes:
        pytest.fail(
            f"{name} expanded no nodes that the tests could see — use expand(problem, node) "
            "from introai.search to generate children",
            pytrace=False,
        )


def test_task_does_not_import_reference_search(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, (
        f"task.py imports {found}: write the functions yourself instead of importing the "
        "course's reference versions"
    )
