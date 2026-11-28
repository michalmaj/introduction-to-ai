"""Small explicit game trees, drawn and traced by hand in the lessons.

A tree has named nodes. MAX moves at the root, and the players alternate with
depth. A move is the name of a child, so ``result(node, child) == child``. A
leaf has a value: its utility for MAX; for MIN it is the negation, so the game
is zero-sum. Internal nodes may also carry ``evaluations``, the estimates a
depth-limited search uses (lesson 3.3).
"""

from __future__ import annotations

import copy
from collections import deque
from collections.abc import Mapping, Sequence

from introai.games.core import Game
from introai.trace import emit


class GameTree(Game):
    """A game given as an explicit tree."""

    players = ("MAX", "MIN")

    def __init__(
        self,
        children: Mapping[str, Sequence[str]],
        leaves: Mapping[str, float],
        root: str,
        evaluations: Mapping[str, float] | None = None,
    ) -> None:
        self.children = {node: list(kids) for node, kids in children.items()}
        self.leaves = dict(leaves)
        self.evaluations = dict(evaluations) if evaluations is not None else None
        both = set(self.children) & set(self.leaves)
        if both:
            raise ValueError(f"a leaf cannot have children: {sorted(both)}")
        if root not in self.children and root not in self.leaves:
            raise ValueError(f"the root {root!r} is not a node of the tree")
        self._depth = {root: 0}
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for child in self.children.get(node, []):
                if child in self._depth:
                    raise ValueError(f"{child!r} is reached twice: this is not a tree")
                if child not in self.children and child not in self.leaves:
                    raise ValueError(f"{child!r} has neither children nor a value")
                self._depth[child] = self._depth[node] + 1
                queue.append(child)
        self.initial = root

    def __repr__(self) -> str:
        return f"GameTree(root={self.initial!r}, nodes={len(self._depth)})"

    def _check(self, node: str) -> None:
        if node not in self._depth:
            raise ValueError(f"{node!r} is not a node of this tree")

    def subtree(self, node: str) -> GameTree:
        """The same tree, started at ``node``; every node keeps its player."""
        self._check(node)
        tree = copy.copy(self)
        tree.initial = node
        return tree

    def depth(self, node: str) -> int:
        """How many moves below the root of the whole tree ``node`` lies."""
        self._check(node)
        return self._depth[node]

    def to_move(self, state: str) -> str:
        return "MAX" if self.depth(state) % 2 == 0 else "MIN"

    def actions(self, state: str) -> list[str]:
        self._check(state)
        return list(self.children.get(state, []))

    def result(self, state: str, action: str) -> str:
        emit("result", state=state, action=action)
        if action not in self.children.get(state, []):
            raise ValueError(f"{action!r} is not a child of {state!r}")
        return action

    def is_terminal(self, state: str) -> bool:
        self._check(state)
        return state in self.leaves

    def utility(self, state: str, player: str) -> float:
        """The leaf value for MAX, its negation for MIN."""
        emit("utility", state=state)
        if state not in self.leaves:
            raise ValueError(f"utility is defined only at a leaf, and {state!r} is not one")
        return self.leaves[state] if player == "MAX" else -self.leaves[state]
