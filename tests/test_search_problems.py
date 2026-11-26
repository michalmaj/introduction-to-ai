import pytest

from introai.search.examples import (
    EXAMPLES,
    EXERCISE_EXAMPLES,
    HEURISTICS,
    binary_tree,
    cyclic,
    disconnected,
    exercise,
    worked_example,
)
from introai.search.problems import GraphProblem


def test_undirected_adjacency_is_sorted():
    assert exercise().actions("E") == ["D", "F", "G"]
    assert worked_example().edges() == [
        ("A", "C"),
        ("A", "S"),
        ("B", "C"),
        ("B", "D"),
        ("B", "S"),
        ("C", "G"),
        ("D", "G"),
    ]


def test_directed_edges_keep_direction_and_order():
    assert binary_tree().edges()[:3] == [("R", "A"), ("R", "B"), ("A", "C")]
    assert binary_tree().actions("G") == []


def test_result_moves_to_neighbour():
    assert exercise().result("A", "B") == "B"


def test_result_rejects_non_neighbour():
    with pytest.raises(ValueError):
        exercise().result("A", "H")


def test_goal_none_is_never_goal():
    assert not cyclic().is_goal("A")


def test_goal_is_recognised():
    p = disconnected()
    assert p.initial == "A" and p.is_goal("D") and not p.is_goal("C")


def test_unit_action_cost():
    assert exercise().action_cost("A", "B", "B") == 1.0


def test_undirected_constructor():
    p = GraphProblem.undirected([("B", "A"), ("A", "C")], "A", "C")
    assert p.actions("A") == ["B", "C"]
    assert p.actions("B") == ["A"]
    assert not p.directed


def test_examples_registry():
    assert set(EXAMPLES) == {
        "worked_example",
        "exercise",
        "binary_tree",
        "cyclic",
        "disconnected",
        "weighted_example",
        "weighted_exercise",
    }
    assert EXERCISE_EXAMPLES == frozenset({"exercise", "weighted_exercise"})
    assert binary_tree().directed and not cyclic().directed


def test_weighted_graph_costs():
    p = GraphProblem.undirected_weighted([("A", "B", 2.5), ("B", "C", 1)], "A", "C")
    assert p.action_cost("A", "B", "B") == 2.5 and p.action_cost("B", "A", "A") == 2.5
    assert p.actions("B") == ["A", "C"]
    assert p.edges() == [("A", "B"), ("B", "C")]
    assert p.weight("B", "C") == 1


def test_unweighted_graph_costs_one():
    assert exercise().action_cost("A", "B", "B") == 1.0


def test_weighted_examples():
    we = EXAMPLES["weighted_example"]()
    assert (we.initial, we.goal) == ("S", "G")
    assert we.action_cost("S", "B", "B") == 6 and we.action_cost("D", "G", "G") == 1
    wx = EXAMPLES["weighted_exercise"]()
    assert (wx.initial, wx.goal) == ("A", "H") and wx.action_cost("E", "G", "G") == 5


@pytest.mark.parametrize("name", ["weighted_example", "weighted_exercise"])
def test_example_heuristics_are_consistent(name):
    problem, h = EXAMPLES[name](), HEURISTICS[name]
    assert h[problem.goal] == 0
    for a, b in problem.edges():
        cost = problem.weight(a, b)
        assert h[a] <= cost + h[b] and h[b] <= cost + h[a], (a, b)
