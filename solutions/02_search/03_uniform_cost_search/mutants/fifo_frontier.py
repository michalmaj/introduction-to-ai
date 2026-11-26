"""Mutant: the frontier is a FIFO queue instead of a priority queue.

Violated requirement: UCS always expands the cheapest node in the frontier.
Common mistake in the lesson: "A queue instead of a priority queue".
"""

import itertools
from collections import deque

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_ucs_expands_in_nondecreasing_path_cost",)

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
    frontier = deque([(root.path_cost, next(counter), root)])
    reached = {root.state: root.path_cost}  # state -> the cheapest path cost found so far
    while frontier:
        cost, _, node = frontier.popleft()
        if cost > reached[node.state]:
            continue  # out of date: a cheaper path to this state was found later
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                frontier.append((child.path_cost, next(counter), child))
    return None
