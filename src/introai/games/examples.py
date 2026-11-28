"""Game trees and positions used in lessons, exercises and tests.

``worked_tree`` is traced step by step in the lessons. ``minimax_exercise`` and
``alpha_beta_exercise`` are the trees students work through by hand, so their
values and traces must never appear in lesson pages (see ``GAME_EXERCISES``).
"""

from __future__ import annotations

import random
from collections.abc import Callable

from introai.games.trees import GameTree


def _tree(spec, evaluations=None) -> GameTree:
    """Build a tree from nested ``(name, value)`` and ``(name, [children])`` pairs."""
    children: dict[str, list[str]] = {}
    leaves: dict[str, float] = {}

    def walk(name, sub):
        if isinstance(sub, list):
            children[name] = [child for child, _ in sub]
            for child, grandchildren in sub:
                walk(child, grandchildren)
        else:
            leaves[name] = sub

    walk(*spec)
    return GameTree(children, leaves, spec[0], evaluations)


def worked_tree() -> GameTree:
    """Two moves deep, three choices each: traced in the lessons on minimax and alpha-beta."""
    return _tree(
        (
            "A",
            [
                ("B", [("B1", 4), ("B2", 9), ("B3", 6)]),
                ("C", [("C1", 2), ("C2", 7), ("C3", 1)]),
                ("D", [("D1", 5), ("D2", 3), ("D3", 8)]),
            ],
        )
    )


def minimax_exercise() -> GameTree:
    """The tree students solve by hand in lesson 3.1, Part A."""
    return _tree(
        (
            "A",
            [
                ("B", [("D", [("H", 3), ("I", 7)]), ("E", [("J", 5), ("K", 1)])]),
                ("C", [("F", [("L", 2), ("M", 6)]), ("G", [("N", 9), ("O", 4)])]),
            ],
        )
    )


def alpha_beta_exercise() -> GameTree:
    """The tree students prune by hand in lesson 3.2, Part A."""
    return _tree(
        (
            "A",
            [
                ("B", [("E", [("K", 3), ("L", 6)]), ("F", [("M", 7), ("N", 2)])]),
                ("C", [("G", [("O", 5), ("P", 8)]), ("H", [("Q", 1), ("R", 4)])]),
                ("D", [("I", [("S", 2), ("T", 1)]), ("J", [("U", 9), ("V", 6)])]),
            ],
        )
    )


def ties_tree() -> GameTree:
    """Equal values: alpha-beta with ``>=`` prunes C2, with ``>`` it prunes nothing."""
    return _tree(("A", [("B", [("B1", 3), ("B2", 5)]), ("C", [("C1", 3), ("C2", 9)])]))


def evaluation_tree() -> GameTree:
    """The worked tree with estimates of B, C and D that mislead a one-move search."""
    tree = worked_tree()
    tree.evaluations = {"B": 5, "C": 2, "D": 6}
    return tree


def cutoff_tree() -> GameTree:
    """Three moves deep, with an estimate at every inner node.

    Searches cut off at depth 1, 2 and 3 all return different values.
    """
    return _tree(
        (
            "A",
            [
                ("B", [("D", [("H", 5), ("I", 1)]), ("E", [("J", 8), ("K", 6)])]),
                ("C", [("F", [("L", 3), ("M", 2)]), ("G", [("N", 9), ("O", 7)])]),
            ],
        ),
        evaluations={"A": 4, "B": 6, "C": 3, "D": 2, "E": 7, "F": 5, "G": 4},
    )


def random_game_tree(branching: int, depth: int, seed: int) -> GameTree:
    """A full tree whose leaf values are 1, 2, ..., branching**depth in a random order.

    Nodes are named by their path: ``"r"``, ``"r.0"``, ``"r.0.2"``, ... All leaf
    values differ, so no two moves ever tie.
    """
    rng = random.Random(seed)
    values = list(range(1, branching**depth + 1))
    rng.shuffle(values)
    children: dict[str, list[str]] = {}
    level = ["r"]
    for _ in range(depth):
        next_level = []
        for node in level:
            children[node] = [f"{node}.{i}" for i in range(branching)]
            next_level += children[node]
        level = next_level
    return GameTree(children, dict(zip(level, values, strict=True)), "r")


def tree_evaluation(game: GameTree, state: str, player: str) -> float:
    """The estimate stored in a tree for an inner node, negated for MIN."""
    if game.is_terminal(state):
        raise ValueError(
            f"{state!r} is a leaf: a terminal state gets its utility, not an evaluation"
        )
    if not game.evaluations or state not in game.evaluations:
        raise ValueError(f"this tree has no evaluation for {state!r}")
    value = game.evaluations[state]
    return value if player == "MAX" else -value


TIC_TAC_TOE_POSITIONS: dict[str, tuple[str, ...]] = {
    "win_now": ("X.X", "OO.", "..."),
    "block": ("X..", ".OX", ".O."),
    "fork": ("XO.", ".X.", "..O"),
    "o_to_move": (".X.", ".O.", ".X."),
    "draw": ("X..", ".O.", "..."),
}
"""Tic-tac-toe positions the tests search (X to move, except in ``o_to_move``)."""

GAME_EXAMPLES: dict[str, Callable[[], GameTree]] = {
    "worked_tree": worked_tree,
    "minimax_exercise": minimax_exercise,
    "alpha_beta_exercise": alpha_beta_exercise,
    "ties_tree": ties_tree,
    "evaluation_tree": evaluation_tree,
    "cutoff_tree": cutoff_tree,
}

GAME_EXERCISES: frozenset[str] = frozenset({"minimax_exercise", "alpha_beta_exercise"})
"""Trees students solve by hand: lesson pages must not show their values or traces."""
