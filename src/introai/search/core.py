"""The vocabulary of search: problems, nodes and expansion.

The names follow the standard notation of the literature (Russell & Norvig):
a problem has an ``initial`` state, ``actions``, a transition model ``result``,
a goal test ``is_goal`` and an ``action_cost``. A search algorithm builds a tree
of :class:`Node` objects by repeatedly calling :func:`expand`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable, Sequence
from dataclasses import dataclass

from introai.trace import emit

State = Hashable
Action = Hashable

CUTOFF = "cutoff"
"""What depth-limited search returns when it stopped at the limit (lesson 2.6).

It means "no goal within the limit, but there may be one deeper", unlike ``None``,
which means "no goal at all".
"""


class Problem(ABC):
    """A search problem: where we start, what we can do and when we are done."""

    def __init__(self, initial: State) -> None:
        self.initial = initial

    @abstractmethod
    def actions(self, state: State) -> Sequence[Action]:
        """The actions available in ``state``, in a fixed order."""

    @abstractmethod
    def result(self, state: State, action: Action) -> State:
        """The state reached by doing ``action`` in ``state``."""

    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Whether ``state`` is a goal state."""

    def action_cost(self, state: State, action: Action, next_state: State) -> float:
        """The cost of one step; every step costs 1 unless a problem says otherwise."""
        return 1.0


@dataclass(frozen=True, eq=False)
class Node:
    """A node of the search tree: a state plus how we got there."""

    state: State
    parent: Node | None = None
    action: Action | None = None
    path_cost: float = 0.0
    depth: int = 0

    def path(self) -> list[Node]:
        """The nodes from the root to this node, root first."""
        nodes: list[Node] = []
        node: Node | None = self
        while node is not None:
            nodes.append(node)
            node = node.parent
        nodes.reverse()
        return nodes

    def solution(self) -> list[Action]:
        """The actions that lead from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def states(self) -> list[State]:
        """The states from the root to this node, root first."""
        return [node.state for node in self.path()]


def expand(problem: Problem, node: Node) -> list[Node]:
    """Generate the children of ``node``, in the order of ``problem.actions``.

    Every call is reported as an ``"expand"`` event, so tests and experiments can
    see which nodes your algorithm expanded and in what order.
    """
    emit("expand", node=node)
    children = []
    for action in problem.actions(node.state):
        next_state = problem.result(node.state, action)
        cost = node.path_cost + problem.action_cost(node.state, action, next_state)
        children.append(Node(next_state, node, action, cost, node.depth + 1))
    return children
