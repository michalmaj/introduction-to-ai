"""Self-check for lesson 2.4: heuristics, greedy best-first search and A*.

Run from the repository root:

    uv run pytest modules/02_search/04_heuristics_and_a_star

The tests check properties every correct implementation has (exact Manhattan
distances, valid paths, the cheapest cost for A*, expansions in order of
non-decreasing f), not one particular way of writing the code. The lesson's
"What the tests do not check" section lists what is left for you to judge.
"""

from pathlib import Path

import pytest

from introai.search.examples import (
    HEURISTICS,
    astar_exercise,
    cyclic,
    disconnected,
    weighted_example,
    weighted_exercise,
    worked_example,
)
from introai.search.problems import GraphProblem
from introai.search.reference import a_star as reference_a_star
from introai.search.reference import greedy_best_first as reference_greedy
from introai.search.reference import ucs as reference_ucs
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.search import assert_valid_solution, expanded_nodes, first_decrease
from introai.trace import TraceLimitExceeded, record
from introai.world.reference import manhattan as reference_manhattan
from introai.world.warehouse import RouteProblem, WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
LIMIT = 10_000  # expansions
STEP_BUDGET = 500_000  # lines executed in task.py during one search
TIE_HINT = (
    "Python compared two Node objects, which it cannot do: when two entries in the heap "
    "have the same priority, heapq compares the next item of the tuples. Put a counter "
    "between the priority and the node, for example (f, next(counter), node)"
)


def table(name):
    values = HEURISTICS[name]
    return lambda state: values[state]


def to_dock(warehouse):
    return lambda cell: reference_manhattan(cell, warehouse.dock)


def zero(state):
    return 0


def warehouse(name):
    return WarehouseMap.from_file(MAPS / f"{name}.txt")


def route(name):
    """A route problem on a map, with the course's Manhattan distance to the dock."""
    w = warehouse(name)
    return RouteProblem(w), to_dock(w)


# name -> (problem, heuristic); the heuristics are the course's, so a bug in your
# manhattan does not make the A* tests fail too.
PROBLEMS = {
    "weighted_example": lambda: (weighted_example(), table("weighted_example")),
    "weighted_exercise": lambda: (weighted_exercise(), table("weighted_exercise")),
    "unit_costs": lambda: (worked_example(), zero),
    "congested_map": lambda: route("congested"),
    "aisles_map": lambda: route("aisles"),
}


def search(impl, name, problem, h, limit=LIMIT, hint=""):
    """Run impl.<name>(problem, h), recording its expansions; turn hangs into failures."""
    failure = None
    try:
        with record(limit=limit) as trace, step_budget(impl.__file__, STEP_BUDGET):
            result = getattr(impl, name)(problem, h)
    except (TraceLimitExceeded, RecursionError):
        failure = (
            f"{name} made more than {limit} expansions {hint}— do you keep track of the "
            "states you have already reached?"
        )
    except StepBudgetExceeded:
        failure = (
            f"{name} ran for too long without finishing — is there a loop that never ends, "
            "for example one that looks at the frontier without removing a node?"
        )
    except TypeError as error:
        if "not supported between instances" not in str(error):
            raise
        failure = TIE_HINT
    if failure:
        pytest.fail(failure, pytrace=False)
    return result, expanded_nodes(trace)


# --- Part A: hand-traced answers -------------------------------------------------------


def reference_answers():
    h = table("astar_exercise")
    greedy = reference_greedy(astar_exercise(), h)
    with record() as trace:
        node = reference_a_star(astar_exercise(), h)
    return greedy.states(), [n.state for n in expanded_nodes(trace)], node.states()


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


def test_part_a_greedy_path(impl):
    check_part_a(impl.GREEDY_PATH, reference_answers()[0], "GREEDY_PATH")


def test_part_a_astar_expansion_order(impl):
    check_part_a(impl.ASTAR_EXPANSION_ORDER, reference_answers()[1], "ASTAR_EXPANSION_ORDER")


def test_part_a_astar_path(impl):
    check_part_a(impl.ASTAR_PATH, reference_answers()[2], "ASTAR_PATH")


# --- Part B: the Manhattan distance ----------------------------------------------------


@pytest.mark.parametrize(
    "cell, goal",
    [((3, 10), (3, 10)), ((1, 1), (3, 4)), ((5, 2), (1, 7)), ((13, 3), (1, 12)), ((0, 9), (0, 2))],
)
def test_manhattan_values(impl, cell, goal):
    expected = reference_manhattan(cell, goal)
    value = impl.manhattan(cell, goal)
    assert value == expected, (
        f"manhattan({cell}, {goal}) returned {value!r}, but the robot needs at least "
        f"{expected} moves: the number of rows plus the number of columns between the cells"
    )


# --- Part B: A* ------------------------------------------------------------------------


def test_a_star_returns_root_when_start_is_goal(impl):
    problem = GraphProblem.undirected_weighted([("A", "B", 1)], "A", "A")
    result, _ = search(impl, "a_star", problem, zero)
    if result is None:
        pytest.fail("a_star returned None, but the start state is already the goal", pytrace=False)
    assert_valid_solution(problem, result)
    assert result.states() == ["A"], "the start state is the goal: return the root node"


@pytest.mark.parametrize("name", PROBLEMS)
def test_a_star_finds_the_cheapest_path(impl, name):
    problem, h = PROBLEMS[name]()
    result, _ = search(impl, "a_star", problem, h)
    if result is None:
        pytest.fail(f"a_star returned None on {name}, but a path to the goal exists", pytrace=False)
    assert_valid_solution(problem, result)
    cheapest = reference_ucs(PROBLEMS[name]()[0]).path_cost
    if result.path_cost > cheapest + 1e-9:
        # The cheapest cost is not printed: on the exercise graph it would be a hint.
        pytest.fail(
            f"a_star found a path of cost {result.path_cost:g} on {name}, but a cheaper one "
            "exists. Is the priority f = g + h (not h alone), and do you test for the goal "
            "when a node is removed from the frontier?",
            pytrace=False,
        )


@pytest.mark.parametrize("name", ["weighted_example", "congested_map"])
def test_a_star_expands_in_nondecreasing_f(impl, name):
    problem, h = PROBLEMS[name]()
    _, nodes = search(impl, "a_star", problem, h)
    violation = first_decrease(nodes, key=lambda node: node.path_cost + h(node.state))
    if violation:
        _, before, after = violation
        f_before = before.path_cost + h(before.state)
        f_after = after.path_cost + h(after.state)
        pytest.fail(
            f"on {name} a_star expanded {after.state} (f = {f_after:g}) right after "
            f"{before.state} (f = {f_before:g}). With a consistent heuristic A* expands nodes "
            "in order of non-decreasing f = g + h — is the frontier ordered by g + h?",
            pytrace=False,
        )


def test_a_star_expands_fewer_nodes_than_ucs(impl):
    problem, h = route("congested")
    result, nodes = search(impl, "a_star", problem, h)
    if result is None:
        pytest.fail("a_star returned None on congested_map, but a route exists", pytrace=False)
    best = reference_ucs(route("congested")[0]).path_cost
    for node in nodes:
        f = node.path_cost + h(node.state)
        if f > best + 1e-9:
            pytest.fail(
                f"a_star expanded the cell {node.state} with f = g + h = {f:g}, more than the "
                f"cost of the best route ({best:g}). A* with an admissible heuristic never needs "
                "such a node — does the priority include h?",
                pytrace=False,
            )
    with record(kinds={"expand"}) as trace:
        reference_ucs(route("congested")[0])
    ucs_count = len(trace.of_kind("expand"))
    assert len(nodes) < ucs_count, (
        f"a_star expanded {len(nodes)} cells, uniform-cost search {ucs_count}: the heuristic "
        "should save work"
    )


@pytest.mark.parametrize("name", ["weighted_example", "congested_map"])
def test_a_star_with_zero_heuristic_costs_as_much_as_ucs(impl, name):
    problem, _ = PROBLEMS[name]()
    result, _ = search(impl, "a_star", problem, zero)
    if result is None:
        pytest.fail(f"a_star with h = 0 returned None on {name}", pytrace=False)
    assert_valid_solution(problem, result)
    cheapest = reference_ucs(PROBLEMS[name]()[0]).path_cost
    assert abs(result.path_cost - cheapest) < 1e-9, (
        f"with h = 0, A* is uniform-cost search and must find cost {cheapest:g} on {name}, "
        f"not {result.path_cost:g}"
    )


def test_a_star_terminates_on_a_graph_with_cycles(impl):
    result, nodes = search(impl, "a_star", cyclic(), zero, limit=1000, hint="on a 4-state graph ")
    assert result is None, "this graph has no goal, so a_star must return None"
    assert {node.state for node in nodes} == {"A", "B", "C", "D"}, (
        "with no goal a_star must expand every reachable state before it gives up"
    )


def test_a_star_returns_none_when_goal_unreachable(impl):
    result, _ = search(impl, "a_star", disconnected(), zero)
    assert result is None, "the goal cannot be reached from the start, so a_star must return None"


# --- Part B: greedy best-first search --------------------------------------------------


@pytest.mark.parametrize("name", ["weighted_example", "congested_map", "aisles_map"])
def test_greedy_returns_a_valid_path(impl, name):
    problem, h = PROBLEMS[name]()
    result, _ = search(impl, "greedy_best_first", problem, h)
    if result is None:
        pytest.fail(
            f"greedy_best_first returned None on {name}, but a path to the goal exists",
            pytrace=False,
        )
    assert_valid_solution(problem, result)


def test_greedy_is_led_by_the_heuristic_alone(impl):
    problem, h = route("congested")
    result, nodes = search(impl, "greedy_best_first", problem, h)
    if result is None:
        pytest.fail("greedy_best_first returned None on congested_map", pytrace=False)
    expected = reference_greedy(*route("congested"))
    assert result.path_cost == expected.path_cost, (
        f"on congested_map greedy best-first should drive straight along the slow corridor "
        f"(cost {expected.path_cost:g}), because every step there gets closer to the dock; "
        f"yours found a route of cost {result.path_cost:g}. Is the priority h alone, "
        "without the path cost g?"
    )
    assert len(nodes) <= len(expected.path()) - 1, (
        f"greedy best-first expanded {len(nodes)} cells; following the heuristic it needs "
        f"only {len(expected.path()) - 1}"
    )


def test_greedy_returns_none_when_goal_unreachable(impl):
    result, _ = search(impl, "greedy_best_first", disconnected(), zero)
    assert result is None, (
        "the goal cannot be reached from the start, so greedy_best_first must return None"
    )


# --- Both algorithms -------------------------------------------------------------------


@pytest.mark.parametrize("name", ["greedy_best_first", "a_star"])
def test_task_uses_expand(impl, name):
    _, nodes = search(impl, name, weighted_example(), table("weighted_example"))
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
