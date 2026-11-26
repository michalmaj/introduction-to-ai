"""Mutant: the Manhattan distance is counted twice.

Violated requirement: manhattan returns the exact number of rows plus columns; an
overestimate is not admissible and A* may then miss the cheapest route.
Common mistake in the lesson: "An overestimating heuristic".
"""

import heapq
import itertools
from collections.abc import Callable

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_manhattan_values",)

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
    return 2 * (abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]))


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
    reached = {root.state: root.path_cost}  # state -> the cheapest path cost found so far
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node.path_cost > reached[node.state]:
            continue  # out of date: a cheaper path to this state was found later
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                heapq.heappush(frontier, (f(child), next(counter), child))
    return None
