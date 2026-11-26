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


def weighted_example() -> GraphProblem:
    """A weighted graph traced step by step in the lessons on UCS and A*."""
    edges = [
        ("S", "A", 1),
        ("S", "B", 6),
        ("A", "B", 2),
        ("A", "D", 7),
        ("B", "C", 2),
        ("C", "G", 2),
        ("D", "G", 1),
        ("B", "G", 6),
    ]
    return GraphProblem.undirected_weighted(edges, "S", "G")


def weighted_exercise() -> GraphProblem:
    """The weighted graph students trace by hand in lessons 2.3 and 2.4."""
    edges = [
        ("A", "B", 2),
        ("A", "C", 4),
        ("B", "C", 1),
        ("B", "D", 7),
        ("C", "E", 3),
        ("D", "F", 1),
        ("E", "D", 1),
        ("E", "F", 6),
        ("F", "H", 2),
        ("E", "G", 5),
        ("G", "H", 1),
    ]
    return GraphProblem.undirected_weighted(edges, "A", "H")


# Consistent heuristics (never more than an edge's cost plus the neighbour's estimate).
WEIGHTED_HEURISTIC: dict[str, float] = {"S": 5, "A": 5, "B": 3, "C": 2, "D": 1, "G": 0}
EXERCISE_HEURISTIC: dict[str, float] = {
    "A": 8,
    "B": 7,
    "C": 6,
    "D": 3,
    "E": 4,
    "F": 2,
    "G": 1,
    "H": 0,
}

EXAMPLES: dict[str, Callable[[], GraphProblem]] = {
    "worked_example": worked_example,
    "exercise": exercise,
    "binary_tree": binary_tree,
    "cyclic": cyclic,
    "disconnected": disconnected,
    "weighted_example": weighted_example,
    "weighted_exercise": weighted_exercise,
}

HEURISTICS: dict[str, dict[str, float]] = {
    "weighted_example": WEIGHTED_HEURISTIC,
    "weighted_exercise": EXERCISE_HEURISTIC,
}

EXERCISE_EXAMPLES: frozenset[str] = frozenset({"exercise", "weighted_exercise"})
