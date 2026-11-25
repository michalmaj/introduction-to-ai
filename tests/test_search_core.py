from introai.search import Node, expand
from introai.search.examples import exercise
from introai.trace import record


def test_node_path_solution_states():
    root = Node("A")
    mid = Node("B", root, "B", 1.0, 1)
    leaf = Node("C", mid, "C", 2.0, 2)
    assert [n.state for n in leaf.path()] == ["A", "B", "C"]
    assert leaf.solution() == ["B", "C"]
    assert leaf.states() == ["A", "B", "C"]


def test_root_has_empty_solution():
    root = Node("A")
    assert root.path() == [root]
    assert root.solution() == []
    assert root.states() == ["A"]


def test_expand_returns_children_in_action_order_and_emits():
    p = exercise()
    root = Node(p.initial)
    node_b = Node("B", root, "B", 1.0, 1)
    with record() as t:
        children = expand(p, node_b)
    assert [c.state for c in children] == ["A", "C", "D"]
    assert all(c.parent is node_b for c in children)
    assert [c.action for c in children] == ["A", "C", "D"]
    assert all(c.depth == 2 and c.path_cost == 2.0 for c in children)
    assert [e.data["node"].state for e in t.of_kind("expand")] == ["B"]
