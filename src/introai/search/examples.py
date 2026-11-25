"""Small graphs used in lessons, exercises and tests.

``worked_example`` is traced step by step in the lessons. ``exercise`` is the
graph students trace themselves, so its traces must never appear in lesson
pages (see ``EXERCISE_EXAMPLES``).
"""

from __future__ import annotations

from collections.abc import Callable

from introai.search.problems import GraphProblem


def worked_example() -> GraphProblem:
    """The graph traced step by step in the lesson text."""
    edges = [("S", "A"), ("S", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "G"), ("D", "G")]
    return GraphProblem.undirected(edges, "S", "G")


def exercise() -> GraphProblem:
    """The graph students trace by hand in Part A."""
    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "C"),
        ("B", "D"),
        ("C", "F"),
        ("D", "E"),
        ("E", "F"),
        ("E", "G"),
        ("F", "H"),
        ("G", "H"),
    ]
    return GraphProblem.undirected(edges, "A", "H")


def binary_tree() -> GraphProblem:
    """A complete binary tree of depth 3 with no goal: searches visit every node."""
    adjacency = {
        "R": ["A", "B"],
        "A": ["C", "D"],
        "B": ["E", "F"],
        "C": ["G", "H"],
        "D": ["I", "J"],
        "E": ["K", "L"],
        "F": ["M", "N"],
    }
    return GraphProblem(adjacency, "R", None)


def cyclic() -> GraphProblem:
    """A small graph full of cycles and with no goal."""
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")]
    return GraphProblem.undirected(edges, "A", None)


def disconnected() -> GraphProblem:
    """Two separate pieces: the goal cannot be reached from the start."""
    return GraphProblem.undirected([("A", "B"), ("C", "D")], "A", "D")


EXAMPLES: dict[str, Callable[[], GraphProblem]] = {
    "worked_example": worked_example,
    "exercise": exercise,
    "binary_tree": binary_tree,
    "cyclic": cyclic,
    "disconnected": disconnected,
}

EXERCISE_EXAMPLES: frozenset[str] = frozenset({"exercise"})
