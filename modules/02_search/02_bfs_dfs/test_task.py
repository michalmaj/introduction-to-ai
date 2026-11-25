"""Self-check for lesson 2.2: breadth-first and depth-first search.

Run from the repository root:

    uv run pytest modules/02_search/02_bfs_dfs

The tests check properties every correct implementation has (valid paths,
shortest paths for BFS, the order in which nodes are expanded), not one
particular way of writing the code. The lesson's "What the tests do not check"
section lists what is left for you to judge.
"""

from pathlib import Path

import pytest

from introai.search.examples import binary_tree, cyclic, disconnected, exercise, worked_example
from introai.search.problems import GraphProblem
from introai.search.reference import bfs as reference_bfs
from introai.search.reference import dfs as reference_dfs
from introai.testing.ast_checks import find_reference_imports
from introai.testing.search import (
    assert_valid_solution,
    duplicate_expansions,
    expanded_nodes,
    first_depth_decrease,
    first_lifo_violation,
)
from introai.trace import TraceLimitExceeded, record
from introai.world.warehouse import RouteProblem, WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
LIMIT = 10_000

PROBLEMS = {
    "worked_example": worked_example,
    "exercise": exercise,
    "small_map": lambda: RouteProblem(WarehouseMap.from_file(MAPS / "small.txt")),
    "aisles_map": lambda: RouteProblem(WarehouseMap.from_file(MAPS / "aisles.txt")),
}


def search(algorithm, problem, limit=LIMIT, hint=""):
    """Run a search, recording its expansions; turn endless loops into failures."""
    try:
        with record(limit=limit) as trace:
            result = algorithm(problem)
    except (TraceLimitExceeded, RecursionError):
        pytest.fail(
            f"{algorithm.__name__} made more than {limit} expansions {hint}(or recursed too "
            "deeply) — do you keep track of the states you have already reached or expanded?"
        )
    return result, expanded_nodes(trace)


# --- Part A: hand-traced answers -------------------------------------------------------


def reference_answer(algorithm):
    with record() as trace:
        node = algorithm(exercise())
    return [n.state for n in expanded_nodes(trace)], node.states()


def check_part_a(value, expected, name):
    if value is None:
        pytest.fail(f"Part A: fill in {name} in task.py")
    if list(value) != expected:
        # Deliberately no diff: the message must not reveal the answer.
        pytest.fail(
            f"Part A: {name} is not right yet (the correct list has {len(expected)} states). "
            "Trace the exercise graph again, following the rules in the lesson."
        )


def test_part_a_bfs_expansion_order(impl):
    check_part_a(
        impl.BFS_EXPANSION_ORDER, reference_answer(reference_bfs)[0], "BFS_EXPANSION_ORDER"
    )


def test_part_a_bfs_path(impl):
    check_part_a(impl.BFS_PATH, reference_answer(reference_bfs)[1], "BFS_PATH")


def test_part_a_dfs_expansion_order(impl):
    check_part_a(
        impl.DFS_EXPANSION_ORDER, reference_answer(reference_dfs)[0], "DFS_EXPANSION_ORDER"
    )


def test_part_a_dfs_path(impl):
    check_part_a(impl.DFS_PATH, reference_answer(reference_dfs)[1], "DFS_PATH")


# --- Part B: breadth-first search ------------------------------------------------------


def test_bfs_returns_root_when_start_is_goal(impl):
    problem = GraphProblem.undirected([("A", "B")], "A", "A")
    result, _ = search(impl.bfs, problem)
    if result is None:
        pytest.fail("bfs returned None, but the start state is already the goal — check it first")
    assert_valid_solution(problem, result)
    assert result.states() == ["A"], "the start state is the goal: return the root node"


@pytest.mark.parametrize("name", PROBLEMS)
def test_bfs_returns_valid_shortest_path(impl, name):
    problem = PROBLEMS[name]()
    result, _ = search(impl.bfs, problem)
    if result is None:
        pytest.fail(f"bfs returned None on {name}, but a path to the goal exists")
    assert_valid_solution(problem, result)
    shortest = len(reference_bfs(PROBLEMS[name]()).solution())
    steps = len(result.solution())
    assert steps == shortest, (
        f"bfs found a {steps}-step path on {name}; the shortest has {shortest}"
    )


def test_bfs_returns_none_when_goal_unreachable(impl):
    result, _ = search(impl.bfs, disconnected())
    assert result is None, "the goal cannot be reached from the start, so bfs must return None"


def test_bfs_expands_in_nondecreasing_depth(impl):
    _, nodes = search(impl.bfs, binary_tree())
    violation = first_depth_decrease(nodes)
    if violation:
        _, before, after = violation
        pytest.fail(
            f"BFS expanded a node at depth {after.depth} right after depth {before.depth} "
            "— are you using a FIFO queue?"
        )
    if len(nodes) != 15:
        pytest.fail(
            f"BFS expanded {len(nodes)} nodes of a 15-node tree that has no goal; "
            "it should expand every node exactly once"
        )


def test_bfs_expands_each_state_at_most_once(impl):
    _, nodes = search(impl.bfs, cyclic(), limit=1000, hint="on a 4-state graph ")
    repeated = duplicate_expansions(nodes)
    assert not repeated, (
        f"BFS expanded {sorted(set(repeated))} more than once — a graph search expands "
        "every state at most once"
    )


# --- Part B: depth-first search --------------------------------------------------------


def test_dfs_returns_root_when_start_is_goal(impl):
    problem = GraphProblem.undirected([("A", "B")], "A", "A")
    result, _ = search(impl.dfs, problem)
    if result is None:
        pytest.fail("dfs returned None, but the start state is already the goal")
    assert_valid_solution(problem, result)
    assert result.states() == ["A"], "the start state is the goal: return the root node"


@pytest.mark.parametrize("name", PROBLEMS)
def test_dfs_returns_valid_path(impl, name):
    problem = PROBLEMS[name]()
    result, _ = search(impl.dfs, problem)
    if result is None:
        pytest.fail(f"dfs returned None on {name}, but a path to the goal exists")
    assert_valid_solution(problem, result)


def test_dfs_returns_none_when_goal_unreachable(impl):
    result, _ = search(impl.dfs, disconnected())
    assert result is None, "the goal cannot be reached from the start, so dfs must return None"


def test_dfs_follows_lifo_order(impl):
    _, nodes = search(impl.dfs, binary_tree())
    violation = first_lifo_violation(nodes)
    if violation:
        _, before, after = violation
        pytest.fail(
            f"DFS expanded {after.state} after {before.state}, but {after.state}'s parent is "
            "not on the current path — are you using a LIFO stack?"
        )
    if len(nodes) != 15:
        pytest.fail(
            f"DFS expanded {len(nodes)} nodes of a 15-node tree that has no goal; "
            "it should expand every node exactly once"
        )


def test_dfs_expands_each_state_at_most_once(impl):
    _, nodes = search(impl.dfs, cyclic(), limit=1000, hint="on a 4-state graph ")
    repeated = duplicate_expansions(nodes)
    assert not repeated, (
        f"DFS expanded {sorted(set(repeated))} more than once — a graph search expands "
        "every state at most once"
    )


# --- Both algorithms -------------------------------------------------------------------


@pytest.mark.parametrize("name", ["bfs", "dfs"])
def test_task_uses_expand(impl, name):
    _, nodes = search(getattr(impl, name), exercise())
    if not nodes:
        pytest.fail(
            f"{name} expanded no nodes that the tests could see — use expand(problem, node) "
            "from introai.search to generate children"
        )


def test_task_does_not_import_reference_search(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, (
        f"task.py imports {found}: write the algorithms yourself instead of importing the "
        "course's reference versions"
    )
