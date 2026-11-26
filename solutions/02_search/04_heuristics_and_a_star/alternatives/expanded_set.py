"""Alternative: best-first search with a set of expanded states.

Every child whose state has not been expanded yet goes on the heap; the first copy
of a state that comes off the heap is expanded and later copies are skipped. For A*
this is optimal when the heuristic is consistent, as Manhattan distance is in the
warehouse.
"""

import heapq
import itertools
from collections.abc import Callable

from introai.search import Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: answers for the A* exercise graph.
# ---------------------------------------------------------------------------------------

GREEDY_PATH: list[str] | None = ["A", "D", "G"]
ASTAR_EXPANSION_ORDER: list[str] | None = ["A", "D", "B", "F"]
ASTAR_PATH: list[str] | None = ["A", "B", "F", "G"]


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def manhattan(cell: tuple[int, int], goal: tuple[int, int]) -> int:
    """The Manhattan distance between two cells given as (row, col)."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def greedy_best_first(problem: Problem, h: Callable) -> Node | None:
    """Greedy best-first search: always expand the node whose state has the lowest h."""
    return best_first(problem, lambda node: h(node.state))


def a_star(problem: Problem, h: Callable) -> Node | None:
    """A* search: always expand the node with the lowest f = path cost + h(state)."""
    return best_first(problem, lambda node: node.path_cost + h(node.state))


def best_first(problem: Problem, f: Callable[[Node], float]) -> Node | None:
    """Best-first search: the ucs of lesson 2.3 with the priority f instead of path cost."""
    root = Node(problem.initial)
    counter = itertools.count()  # breaks ties: Node objects cannot be compared
    frontier = [(f(root), next(counter), root)]
    expanded = set()
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node.state in expanded:
            continue
        if problem.is_goal(node.state):
            return node
        expanded.add(node.state)
        for child in expand(problem, node):
            if child.state not in expanded:
                heapq.heappush(frontier, (f(child), next(counter), child))
    return None
