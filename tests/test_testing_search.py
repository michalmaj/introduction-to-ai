import pytest

from introai.search import Node, expand
from introai.search.examples import worked_example
from introai.search.reference import bfs
from introai.testing.search import (
    assert_valid_solution,
    duplicate_expansions,
    expanded_nodes,
    first_depth_decrease,
    first_lifo_violation,
)
from introai.trace import record


def chain(*states):
    node = Node(states[0])
    for state in states[1:]:
        node = Node(state, node, state, node.path_cost + 1.0, node.depth + 1)
    return node


def test_expanded_nodes_reads_expand_events():
    p = worked_example()
    root = Node(p.initial)
    with record() as t:
        expand(p, root)
    assert expanded_nodes(t) == [root]


def test_duplicate_expansions():
    nodes = [Node(s) for s in ["A", "B", "A", "C", "B"]]
    assert duplicate_expansions(nodes) == ["A", "B"]
    assert duplicate_expansions([Node("A"), Node("B")]) == []


def test_first_depth_decrease():
    nodes = [Node("x", depth=d) for d in [0, 1, 1, 2, 1]]
    assert first_depth_decrease(nodes) == (3, nodes[3], nodes[4])
    assert first_depth_decrease(nodes[:4]) is None


def test_first_lifo_violation():
    r = Node("R")
    a = Node("A", r, "A", 1.0, 1)
    b = Node("B", r, "B", 1.0, 1)
    c = Node("C", a, "C", 2.0, 2)
    assert first_lifo_violation([r, a, c, b]) is None
    assert first_lifo_violation([r, a, b, c]) == (2, b, c)


def test_assert_valid_solution_accepts_reference_result():
    p = worked_example()
    assert_valid_solution(p, bfs(p))


def test_assert_valid_solution_rejects_wrong_type():
    p = worked_example()
    with pytest.raises(AssertionError, match=r"must return a Node \(or None\), got list"):
        assert_valid_solution(p, ["S", "A", "C", "G"])


def test_assert_valid_solution_rejects_illegal_action():
    with pytest.raises(AssertionError, match="is not a legal action"):
        assert_valid_solution(worked_example(), chain("S", "G"))


def test_assert_valid_solution_rejects_wrong_start():
    with pytest.raises(AssertionError, match="must start at the initial state"):
        assert_valid_solution(worked_example(), chain("A", "C", "G"))


def test_assert_valid_solution_rejects_non_goal_end():
    with pytest.raises(AssertionError, match="is not a goal state"):
        assert_valid_solution(worked_example(), chain("S", "A"))


def test_assert_valid_solution_rejects_wrong_cost():
    node = chain("S", "A", "C", "G")
    bad = Node("G", node.parent, "G", 99.0, node.depth)
    with pytest.raises(AssertionError, match="path_cost is 99.0"):
        assert_valid_solution(worked_example(), bad)


def test_first_decrease_finds_the_first_drop_in_a_key():
    from introai.search import Node
    from introai.testing.search import first_decrease

    a, b, c, d = Node("A", path_cost=1), Node("B", path_cost=3), Node("C", path_cost=2), Node("D")
    assert first_decrease([a, b, c, d], key=lambda node: node.path_cost) == (1, b, c)
    assert first_decrease([a, b], key=lambda node: node.path_cost) is None
    assert first_decrease([b, Node("E", path_cost=3 - 1e-12)], key=lambda n: n.path_cost) is None
