"""Reference implementations of breadth-first and depth-first search.

These are the course's own versions of the algorithms you implement in the
lessons. Experiments use them, and lesson tests compare your hand-traced
answers with them. Your ``task.py`` must not import this module.

Besides the ``"expand"`` events reported by :func:`introai.search.expand`,
both functions emit ``"step"`` events that describe the frontier after every
step; the lesson pages turn them into step-by-step tables.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from introai.search.core import Node, Problem, State, expand
from introai.trace import emit, wants


def bfs(problem: Problem) -> Node | None:
    """Breadth-first search with an early goal test.

    Rules (they also define the expected answers of hand-traced exercises):

    - if the initial state is a goal, return the root right away;
    - the frontier is a FIFO queue; ``reached`` holds every state seen so far;
    - when expanding a node, a child whose state was already reached is ignored;
    - a new child that is a goal is returned at once (the goal is tested when
      the child is generated, not when it is removed from the frontier).
    """
    root = Node(problem.initial)
    if problem.is_goal(root.state):
        return root

    frontier: deque[Node] = deque([root])
    reached: set[State] = {root.state}

    while frontier:
        node = frontier.popleft()
        for child in expand(problem, node):
            if child.state in reached:
                continue
            if problem.is_goal(child.state):
                if wants("step"):
                    _bfs_step(node, frontier, reached)
                emit("goal", node=child)
                return child
            reached.add(child.state)
            frontier.append(child)
        if wants("step"):  # building step data costs time: only when recorded
            _bfs_step(node, frontier, reached)

    return None


def dfs(problem: Problem) -> Node | None:
    """Depth-first graph search with a late goal test.

    Rules (they also define the expected answers of hand-traced exercises):

    - the frontier is a LIFO stack; ``expanded`` holds every expanded state;
    - a node whose state was already expanded is skipped when it is removed;
    - the goal is tested when a node is removed from the frontier;
    - children are pushed in reverse order, so the child of the first action
      is removed (and expanded) first.
    """
    frontier: list[Node] = [Node(problem.initial)]
    expanded: set[State] = set()

    while frontier:
        node = frontier.pop()
        if node.state in expanded:
            if wants("step"):
                _dfs_step(node, "skipped", frontier, expanded)
            continue
        if problem.is_goal(node.state):
            if wants("step"):
                _dfs_step(node, "goal", frontier, expanded)
            emit("goal", node=node)
            return node
        expanded.add(node.state)
        children = [child for child in expand(problem, node) if child.state not in expanded]
        frontier.extend(reversed(children))
        if wants("step"):
            _dfs_step(node, "expanded", frontier, expanded)

    return None


def _sorted_states(states: Iterable[State]) -> list[State]:
    states = list(states)
    try:
        return sorted(states)
    except TypeError:
        return sorted(states, key=repr)


def _bfs_step(node: Node, frontier: deque[Node], reached: set[State]) -> None:
    emit(
        "step",
        expanded=node.state,
        frontier=[n.state for n in frontier],
        reached=_sorted_states(reached),
    )


def _dfs_step(node: Node, outcome: str, frontier: list[Node], expanded: set[State]) -> None:
    emit(
        "step",
        popped=node.state,
        outcome=outcome,
        frontier=[n.state for n in reversed(frontier)],
        expanded=_sorted_states(expanded),
    )
