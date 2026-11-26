"""Self-check for lesson 2.1: state spaces and search trees.

Run from the repository root:

    uv run pytest modules/02_search/01_state_space

The tests check what every correct expand and count_tree_nodes must do: the
order, parent, action, depth and cost of every child, and the size of each
level of the search tree. The lesson's "What the tests do not check" section
lists what is left for you to judge.
"""

from pathlib import Path

import pytest

from introai.search import Node
from introai.search import expand as course_expand
from introai.search.examples import binary_tree, cyclic, exercise, weighted_example, worked_example
from introai.search.problems import GraphProblem
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.trace import TraceLimitExceeded, record
from introai.world.warehouse import RouteProblem, WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
STEP_BUDGET = 2_000_000  # lines executed in task.py during one call
NODE_HINT = (
    "expand must return a list of Node objects, for example "
    "Node(next_state, node, action, path_cost, node.depth + 1)"
)


def guarded(impl, call, *args):
    """Call student code; turn endless loops into a hint. Returns (result, trace)."""
    name = getattr(call, "__name__", "your function")
    failure = None
    try:
        with record(limit=200_000, kinds={"expand"}) as trace:
            with step_budget(impl.__file__, STEP_BUDGET):
                result = call(*args)
    except (StepBudgetExceeded, TraceLimitExceeded):
        failure = f"{name} ran for too long — is there a loop that never ends?"
    except RecursionError:
        failure = f"{name} recursed too deeply — does every call get closer to the end?"
    if failure:
        pytest.fail(failure, pytrace=False)
    return result, trace


def children_of(impl, problem, node):
    children, _ = guarded(impl, impl.expand, problem, node)
    if children is None:
        pytest.fail(f"expand returned None — {NODE_HINT}", pytrace=False)
    children = list(children)
    if not all(isinstance(child, Node) for child in children):
        pytest.fail(NODE_HINT, pytrace=False)
    return children


def course_levels(problem, depth):
    """The search tree level by level, built with the course's expand."""
    levels = [[Node(problem.initial)]]
    for _ in range(depth):
        levels.append([child for node in levels[-1] for child in course_expand(problem, node)])
    return levels


def counts_of(impl, problem, depth):
    counts, _ = guarded(impl, impl.count_tree_nodes, problem, depth)
    if counts is None:
        pytest.fail("count_tree_nodes returned None — return a list of numbers", pytrace=False)
    counts = list(counts)
    if len(counts) != depth + 1:
        pytest.fail(
            f"count_tree_nodes(problem, {depth}) returned {len(counts)} numbers; it must return "
            f"{depth + 1}, one for each depth 0, 1, ..., {depth} (depth 0 is the root)",
            pytrace=False,
        )
    return counts


# --- Part A: counting by hand ----------------------------------------------------------


def check_number(value, expected, name, hint):
    # pytrace=False: no traceback, so pytest cannot print `expected`. Never reveal it.
    if value is None:
        pytest.fail(f"Part A: fill in {name} in task.py", pytrace=False)
    if isinstance(value, bool) or not isinstance(value, int):
        pytest.fail(f"Part A: {name} must be a whole number, not {value!r}", pytrace=False)
    if value != expected:
        pytest.fail(f"Part A: {name} is not right yet. {hint}", pytrace=False)


def test_part_a_tree_nodes_at_depth_2(impl):
    level = course_levels(exercise(), 2)[2]
    check_number(
        impl.TREE_NODES_AT_DEPTH_2,
        len(level),
        "TREE_NODES_AT_DEPTH_2",
        "Draw the tree down to depth 2: every path from the start is its own node, "
        "even when it leads back to a state that is already in the tree.",
    )


def test_part_a_states_at_depth_2(impl):
    level = course_levels(exercise(), 2)[2]
    check_number(
        impl.STATES_AT_DEPTH_2,
        len({node.state for node in level}),
        "STATES_AT_DEPTH_2",
        "Look at the nodes at depth 2 only and count each state once.",
    )


# --- Part B: expand --------------------------------------------------------------------


def test_expand_is_your_own(impl):
    code = getattr(impl.expand, "__code__", None)
    if code is None or Path(code.co_filename).resolve() != Path(impl.__file__).resolve():
        pytest.fail(
            "expand is not defined in task.py — write it yourself instead of importing it",
            pytrace=False,
        )
    problem = worked_example()
    _, trace = guarded(impl, impl.expand, problem, Node(problem.initial))
    if trace.of_kind("expand"):
        pytest.fail(
            "your expand calls the course's expand from introai.search — write the loop over "
            "problem.actions yourself",
            pytrace=False,
        )


def test_expand_children_follow_the_actions_order(impl):
    problem = worked_example()
    node = Node("B", Node("S"), "B", 1.0, 1)
    states = [child.state for child in children_of(impl, problem, node)]
    expected = [problem.result("B", action) for action in problem.actions("B")]
    assert states == expected, (
        f"the children of B are {states}; expand must create one child per action, in the "
        f"order of problem.actions(state): {expected}"
    )


def test_expand_records_parent_and_action(impl):
    problem = worked_example()
    node = Node("B", Node("S"), "B", 1.0, 1)
    children = children_of(impl, problem, node)
    for child, action in zip(children, problem.actions("B"), strict=False):
        assert child.parent is node, (
            f"the child {child.state} does not point to its parent: pass the node you expand "
            "as the parent, so that node.path() can walk back to the root"
        )
        assert child.action == action, (
            f"the child {child.state} has action {child.action!r}; it must remember the "
            f"action that led to it ({action!r})"
        )


def test_expand_increases_depth(impl):
    problem = worked_example()
    node = Node("C", Node("A", Node("S"), "A", 1.0, 1), "C", 2.0, 2)
    for child in children_of(impl, problem, node):
        assert child.depth == 3, (
            f"a child of a node at depth 2 has depth {child.depth}; a child is one level "
            "deeper than its parent"
        )


def test_expand_accumulates_path_cost(impl):
    problem = weighted_example()  # S-A costs 1, A-B costs 2, so B is reached at cost 3
    node = Node("B", Node("A", Node("S"), "A", 1.0, 1), "B", 3.0, 2)
    expected = {child.state: child.path_cost for child in course_expand(problem, node)}
    for child in children_of(impl, problem, node):
        assert child.path_cost == expected[child.state], (
            f"the child {child.state} of B has path_cost {child.path_cost}, but the path "
            f"S-A-B-{child.state} costs {expected[child.state]}: add the step cost "
            "problem.action_cost(state, action, next_state) to the parent's path_cost"
        )


def test_expand_uses_step_costs_of_the_map(impl):
    problem = RouteProblem(WarehouseMap.from_file(MAPS / "congested.txt"))
    node = Node(problem.initial, path_cost=5.0)  # east of the start lies a slow zone
    expected = {child.state: child.path_cost for child in course_expand(problem, node)}
    children = children_of(impl, problem, node)
    assert {child.state for child in children} == set(expected), (
        "in the warehouse the children are the free neighbouring cells"
    )
    for child in children:
        assert child.path_cost == expected[child.state], (
            f"the step into {child.state} costs {expected[child.state] - 5:g} on this map, so "
            f"the child's path_cost is {expected[child.state]:g}, not {child.path_cost} — "
            "ask the problem for the step cost with problem.action_cost"
        )


def test_expand_of_a_dead_end_is_empty(impl):
    problem = GraphProblem({"A": ["B"], "B": []}, "A", None)
    children = children_of(impl, problem, Node("B", Node("A"), "B", 1.0, 1))
    assert children == [], "a state without actions has no children: expand returns []"


# --- Part B: count_tree_nodes ----------------------------------------------------------


def test_count_tree_nodes_at_depth_0_is_the_root(impl):
    assert counts_of(impl, worked_example(), 0) == [1], (
        "at depth 0 the tree has exactly one node: the root"
    )


def test_count_tree_nodes_on_a_binary_tree(impl):
    expected = [len(level) for level in course_levels(binary_tree(), 3)]
    counts = counts_of(impl, binary_tree(), 3)
    assert counts == expected, (
        f"on a complete binary tree every level has twice as many nodes as the one above: "
        f"expected {expected}, got {counts}"
    )


def test_count_tree_nodes_below_the_leaves_is_zero(impl):
    counts = counts_of(impl, binary_tree(), 4)
    assert counts[4] == 0, (
        f"the binary tree ends at depth 3, so depth 4 has no nodes, not {counts[4]}"
    )


def test_count_tree_nodes_keeps_redundant_paths(impl):
    expected = [len(level) for level in course_levels(cyclic(), 4)]
    counts = counts_of(impl, cyclic(), 4)
    assert counts == expected, (
        f"on a graph with cycles the tree holds the same state many times: expected "
        f"{expected}, got {counts}. Count every node — a tree search keeps no record of "
        "the states it has already seen"
    )


def test_count_tree_nodes_does_not_stop_at_the_goal(impl):
    expected = [len(level) for level in course_levels(worked_example(), 4)]
    counts = counts_of(impl, worked_example(), 4)
    assert counts == expected, (
        f"expected {expected}, got {counts}: the tree grows past the goal G as well — "
        "count_tree_nodes counts the whole tree and never tests for the goal"
    )


def test_count_tree_nodes_in_the_warehouse(impl):
    problem = RouteProblem(WarehouseMap.from_file(MAPS / "aisles.txt"))
    expected = [len(level) for level in course_levels(problem, 8)]
    counts = counts_of(impl, problem, 8)
    assert counts == expected, f"on aisles.txt expected {expected}, got {counts}"


def test_task_does_not_import_reference(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, f"task.py imports {found}: write the functions yourself"
