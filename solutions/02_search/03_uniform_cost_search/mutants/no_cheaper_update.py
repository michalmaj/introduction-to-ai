"""Mutant: a state already reached is never added again, even along a cheaper path.

Violated requirement: when a cheaper path to a reached state is found, UCS keeps it.
Common mistake in the lesson: "No update for a cheaper path".
"""

import heapq
import itertools

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_ucs_finds_the_cheapest_path[weighted_example]",)

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
            if child.state not in reached:
                reached[child.state] = child.path_cost
                heapq.heappush(frontier, (child.path_cost, next(counter), child))
    return None
