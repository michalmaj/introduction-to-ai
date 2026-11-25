import pytest

from introai.search.examples import (
    EXAMPLES,
    EXERCISE_EXAMPLES,
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
    assert set(EXAMPLES) == {"worked_example", "exercise", "binary_tree", "cyclic", "disconnected"}
    assert EXERCISE_EXAMPLES == frozenset({"exercise"})
    assert binary_tree().directed and not cyclic().directed
