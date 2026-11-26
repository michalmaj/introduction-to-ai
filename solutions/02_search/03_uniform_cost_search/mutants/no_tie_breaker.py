"""Mutant: the heap holds (cost, node) pairs with no counter between them.

Violated requirement: ucs must work when two frontier entries have the same cost;
heapq then compares the nodes, and Node objects cannot be compared.
Common mistake in the lesson: "No tie-breaker in the heap".
"""

import heapq

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_ucs_breaks_ties_between_equal_costs",)

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
    frontier = [(root.path_cost, root)]
    reached = {root.state: root.path_cost}  # state -> the cheapest path cost found so far
    while frontier:
        cost, node = heapq.heappop(frontier)
        if cost > reached[node.state]:
            continue  # out of date: a cheaper path to this state was found later
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if child.state not in reached or child.path_cost < reached[child.state]:
                reached[child.state] = child.path_cost
                heapq.heappush(frontier, (child.path_cost, child))
    return None
