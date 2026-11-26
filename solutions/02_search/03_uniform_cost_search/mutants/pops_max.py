"""Mutant: the frontier gives back the most expensive node instead of the cheapest.

Violated requirement: UCS always expands the cheapest node in the frontier.
Common mistake in the lesson: "The most expensive node first".
"""

import heapq
import itertools

from introai.search import Node, Problem, expand

CAUGHT_BY = (
    "test_ucs_finds_the_cheapest_path[weighted_example]",
    "test_ucs_finds_the_cheapest_path[congested_map]",
)

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
    frontier = [(-root.path_cost, next(counter), root)]
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
                heapq.heappush(frontier, (-child.path_cost, next(counter), child))
    return None
