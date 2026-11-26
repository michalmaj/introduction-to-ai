"""Mutant: the goal is tested when a child is generated, as in BFS.

Violated requirement: UCS returns the cheapest path; a goal generated early may still
be reached more cheaply later.
Common mistake in the lesson: "The goal test from BFS".
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
    if problem.is_goal(root.state):
        return root
    counter = itertools.count()  # breaks ties: Node objects cannot be compared
    frontier = [(root.path_cost, next(counter), root)]
    reached = {root.state: root.path_cost}  # state -> the cheapest path cost found so far
    while frontier:
        cost, _, node = heapq.heappop(frontier)
        if cost > reached[node.state]:
            continue  # out of date: a cheaper path to this state was found later
        for child in expand(problem, node):
            if child.state not in reached or child.path_cost < reached[child.state]:
                if problem.is_goal(child.state):
                    return child
                reached[child.state] = child.path_cost
                heapq.heappush(frontier, (child.path_cost, next(counter), child))
    return None
