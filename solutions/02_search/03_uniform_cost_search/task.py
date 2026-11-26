"""Lesson 2.3: uniform-cost search (reference solution).

Do not read this before you have tried the lesson yourself.
"""

import heapq
import itertools

from introai.search import Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: answers for the weighted exercise graph.
# ---------------------------------------------------------------------------------------

UCS_EXPANSION_ORDER: list[str] | None = ["A", "B", "C", "E", "D", "F"]
UCS_PATH: list[str] | None = ["A", "B", "C", "E", "D", "F", "H"]


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def ucs(problem: Problem) -> Node | None:
    """Uniform-cost search: always expand the node with the lowest path cost."""
    root = Node(problem.initial)
    counter = itertools.count()  # breaks ties: Node objects cannot be compared
    frontier = [(root.path_cost, next(counter), root)]
    reached = {root.state: root.path_cost}  # state -> the cheapest path cost found so far
    while frontier:
        cost, _, node = heapq.heappop(frontier)
        if cost > reached[node.state]:
            continue  # out of date: a cheaper path to this state was found later
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                heapq.heappush(frontier, (child.path_cost, next(counter), child))
    return None
