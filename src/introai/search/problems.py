"""Search problems on explicit graphs."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

from introai.search.core import Problem


class GraphProblem(Problem):
    """Find a path in a graph given as adjacency lists.

    An action is the name of the neighbour to move to, so ``result(s, a) == a``.
    Neighbours are tried in the order they appear in the adjacency list.
    """

    def __init__(
        self,
        adjacency: Mapping[str, Sequence[str]],
        initial: str,
        goal: str | None,
        *,
        directed: bool = True,
    ) -> None:
        super().__init__(initial)
        self.adjacency = {state: list(neighbours) for state, neighbours in adjacency.items()}
        self.goal = goal
        self.directed = directed

    @classmethod
    def undirected(
        cls, edges: Iterable[tuple[str, str]], initial: str, goal: str | None
    ) -> GraphProblem:
        """Build an undirected graph; every neighbour list is sorted alphabetically."""
        neighbours: dict[str, set[str]] = {}
        for a, b in edges:
            neighbours.setdefault(a, set()).add(b)
            neighbours.setdefault(b, set()).add(a)
        adjacency = {state: sorted(neighbours[state]) for state in sorted(neighbours)}
        return cls(adjacency, initial, goal, directed=False)

    def actions(self, state: str) -> list[str]:
        return list(self.adjacency.get(state, ()))

    def result(self, state: str, action: str) -> str:
        if action not in self.adjacency.get(state, ()):
            raise ValueError(f"{action!r} is not a neighbour of {state!r}")
        return action

    def is_goal(self, state: str) -> bool:
        return self.goal is not None and state == self.goal

    def edges(self) -> list[tuple[str, str]]:
        """The edges of the graph; for undirected graphs each pair once, sorted."""
        if self.directed:
            return [(a, b) for a, neighbours in self.adjacency.items() for b in neighbours]
        pairs = {
            (min(a, b), max(a, b)) for a, neighbours in self.adjacency.items() for b in neighbours
        }
        return sorted(pairs)
