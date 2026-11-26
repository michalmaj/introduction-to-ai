"""Alternative: Dijkstra's algorithm with a set of expanded states.

Every child whose state has not been expanded yet goes on the heap, so a state can
be there several times. The first time a state comes off the heap it has its
cheapest cost; later copies are skipped.
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
                heapq.heappush(frontier, (child.path_cost, next(counter), child))
    return None
