"""Helpers for testing search algorithms through their trace.

The checks look at properties every correct implementation has, whatever order
it breaks ties in: BFS never goes back to a shallower depth, DFS always
continues from the current path, a graph search expands each state once.
"""

from __future__ import annotations

from collections.abc import Sequence

from introai.search.core import Node, Problem, State
from introai.trace import Trace


def expanded_nodes(trace: Trace) -> list[Node]:
    """The nodes passed to ``expand``, in order."""
    return [event.data["node"] for event in trace.of_kind("expand")]


def duplicate_expansions(nodes: Sequence[Node]) -> list[State]:
    """States expanded more than once, listed at their second and later expansion."""
    seen: set[State] = set()
    duplicates: list[State] = []
    for node in nodes:
        if node.state in seen:
            duplicates.append(node.state)
        seen.add(node.state)
    return duplicates


def first_depth_decrease(nodes: Sequence[Node]) -> tuple[int, Node, Node] | None:
    """The first ``i`` where the next expanded node is shallower than ``nodes[i]``."""
    for i, (current, following) in enumerate(zip(nodes, nodes[1:])):
        if following.depth < current.depth:
            return i, current, following
    return None


def first_lifo_violation(nodes: Sequence[Node]) -> tuple[int, Node, Node] | None:
    """The first ``i`` where the next expanded node does not continue the current path.

    In depth-first search the next node to expand is always a child of some node
    on the path to the node just expanded.
    """
    for i, (current, following) in enumerate(zip(nodes, nodes[1:])):
        if following.parent is not None and following.parent.state not in current.states():
            return i, current, following
    return None


def assert_valid_solution(problem: Problem, node: object) -> None:
    """Check that ``node`` describes a legal path from the start to a goal."""
    if not isinstance(node, Node):
        raise AssertionError(f"the search must return a Node (or None), got {type(node).__name__}")
    path = node.path()
    if path[0].state != problem.initial:
        raise AssertionError(
            f"the path must start at the initial state {problem.initial!r}, "
            f"but starts at {path[0].state!r}"
        )
    total = 0.0
    for step, (previous, current) in enumerate(zip(path, path[1:]), start=1):
        if current.action not in problem.actions(previous.state):
            raise AssertionError(
                f"step {step}: {current.action!r} is not a legal action in state {previous.state!r}"
            )
        expected = problem.result(previous.state, current.action)
        if expected != current.state:
            raise AssertionError(
                f"step {step}: doing {current.action!r} in {previous.state!r} leads to "
                f"{expected!r}, not {current.state!r}"
            )
        total += problem.action_cost(previous.state, current.action, current.state)
    if not problem.is_goal(node.state):
        raise AssertionError(f"the path ends at {node.state!r}, which is not a goal state")
    if abs(node.path_cost - total) > 1e-9:
        raise AssertionError(f"path_cost is {node.path_cost}, but the steps cost {total}")
    if node.depth != len(path) - 1:
        raise AssertionError(f"depth is {node.depth}, but the path has {len(path) - 1} steps")
