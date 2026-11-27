"""Reference implementations of the search algorithms in module 2.

These are the course's own versions of the algorithms you implement in the
lessons. Experiments use them, and lesson tests compare your hand-traced
answers with them. Your ``task.py`` must not import this module.

Besides the ``"expand"`` events reported by :func:`introai.search.expand`,
the search functions emit ``"step"`` events that describe the frontier after every
step; the lesson pages turn them into step-by-step tables.
"""

from __future__ import annotations

import heapq
import itertools
from collections import deque
from collections.abc import Callable, Iterable

from introai.search.core import CUTOFF, Node, Problem, State, expand
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
        if wants("frontier"):
            emit("frontier", size=len(frontier))

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
        if wants("frontier"):
            emit("frontier", size=len(frontier))

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


# --- Best-first search: UCS, greedy best-first and A* ----------------------------------

Heuristic = Callable[[State], float]


def ucs(problem: Problem) -> Node | None:
    """Uniform-cost search: always expand the node with the lowest path cost g."""
    return _best_first(problem, lambda node: node.path_cost)


def greedy_best_first(problem: Problem, h: Heuristic) -> Node | None:
    """Greedy best-first search: always expand the node that looks closest, by h alone."""
    return _best_first(problem, lambda node: h(node.state))


def a_star(problem: Problem, h: Heuristic) -> Node | None:
    """A* search: always expand the node with the lowest f = g + h."""
    return _best_first(problem, lambda node: node.path_cost + h(node.state))


def _best_first(problem: Problem, priority: Callable[[Node], float]) -> Node | None:
    """The shared core of UCS, greedy best-first and A*.

    Rules (they also define the expected answers of hand-traced exercises):

    - the frontier is a priority queue ordered by ``priority``; ties are broken
      by insertion order (the node added first is removed first);
    - ``reached`` maps every state to the lowest path cost found so far; a child
      is added only if its state is new or reached more cheaply than before;
    - a removed node whose path cost is higher than the best known one is a
      stale entry and is skipped;
    - the goal is tested when a node is removed from the frontier.
    """
    root = Node(problem.initial)
    counter = itertools.count()
    frontier: list[tuple[float, int, Node]] = [(priority(root), next(counter), root)]
    reached: dict[State, float] = {root.state: root.path_cost}

    while frontier:
        f, _, node = heapq.heappop(frontier)
        if node.path_cost > reached[node.state]:
            if wants("step"):
                _best_first_step(node, f, "skipped", frontier, reached)
            continue
        if problem.is_goal(node.state):
            if wants("step"):
                _best_first_step(node, f, "goal", frontier, reached)
            emit("goal", node=node)
            return node
        for child in expand(problem, node):
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                heapq.heappush(frontier, (priority(child), next(counter), child))
        if wants("step"):
            _best_first_step(node, f, "expanded", frontier, reached)
        if wants("frontier"):
            emit("frontier", size=len(frontier))

    return None


def _best_first_step(
    node: Node,
    f: float,
    outcome: str,
    frontier: list[tuple[float, int, Node]],
    reached: dict[State, float],
) -> None:
    emit(
        "step",
        popped=node.state,
        outcome=outcome,
        g=node.path_cost,
        f=f,
        frontier=[(n.state, priority) for priority, _, n in sorted(frontier)],
        reached=[(state, reached[state]) for state in _sorted_states(reached)],
    )


def count_tree_nodes(problem: Problem, depth: int) -> list[int]:
    """The number of search tree nodes at each depth 0, 1, ..., ``depth`` (lesson 2.1).

    The tree keeps every path and has no goal test. Nodes at the same depth with
    the same state have identical subtrees, so it is enough to count, for each
    state, how many nodes at the current depth hold it.
    """
    level = {problem.initial: 1}
    counts = [1]
    for _ in range(depth):
        next_level: dict[State, int] = {}
        for state, paths in level.items():
            for action in problem.actions(state):
                child = problem.result(state, action)
                next_level[child] = next_level.get(child, 0) + paths
        level = next_level
        counts.append(sum(level.values()))
    return counts


# --- Depth-limited search and iterative deepening (lesson 2.6) ------------------------


def depth_limited_search(problem: Problem, limit: int) -> Node | None | str:
    """Depth-first tree search that does not go deeper than ``limit``.

    Rules (they also define the expected answers of hand-traced exercises):

    - the frontier is a LIFO stack; children are pushed in reverse order, so the
      child of the first action is removed first;
    - a removed node is goal-tested first; then a node at depth ``limit`` or
      deeper is cut off, and a node whose state appears among its ancestors (a
      cycle) is not expanded; any other node is expanded;
    - returns the goal node, ``CUTOFF`` if some node was cut off, otherwise ``None``.
    """
    frontier: list[Node] = [Node(problem.initial)]
    result: Node | None | str = None
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            outcome = "goal"
        elif node.depth >= limit:
            outcome = "cutoff"
            result = CUTOFF
        elif _is_cycle(node):
            outcome = "cycle"
        else:
            outcome = "expanded"
            frontier.extend(reversed(expand(problem, node)))
        if wants("step"):
            emit(
                "step",
                limit=limit,
                popped=node.state,
                depth=node.depth,
                outcome=outcome,
                stack=[n.state for n in reversed(frontier)],
            )
        if outcome == "goal":
            emit("goal", node=node)
            return node
        if wants("frontier"):
            emit("frontier", size=len(frontier))
    return result


def iterative_deepening_search(problem: Problem) -> Node | None:
    """Depth-limited search with the limits 0, 1, 2, ... until the result is not ``CUTOFF``."""
    limit = 0
    while True:
        result = depth_limited_search(problem, limit)
        emit("iteration", limit=limit, result=result)
        if result is not CUTOFF:
            return result
        limit += 1


def _is_cycle(node: Node) -> bool:
    ancestor = node.parent
    while ancestor is not None:
        if ancestor.state == node.state:
            return True
        ancestor = ancestor.parent
    return False


# --- Properties of the strategies (lesson 2.5) -----------------------------------------

STRATEGY_PROPERTIES: dict[str, dict[str, bool]] = {
    # Graph searches as written in this course. Assumptions, as in lesson 2.5:
    # complete_finite: finite state space; complete_infinite: infinite state space,
    # finite branching factor, every step costs at least some eps > 0, a solution
    # exists; A* uses an admissible heuristic; optimal_any_costs: positive step costs.
    "BFS": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": False,
    },
    "DFS": {
        "complete_finite": True,
        "complete_infinite": False,
        "optimal_unit_costs": False,
        "optimal_any_costs": False,
    },
    "UCS": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": True,
    },
    "greedy": {
        "complete_finite": True,
        "complete_infinite": False,
        "optimal_unit_costs": False,
        "optimal_any_costs": False,
    },
    "A*": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": True,
    },
}
