"""Alternative: the version from Russell and Norvig (figure 3.7), with no skipping.

reached maps each state to its best node. An out-of-date frontier entry is not
skipped: it is expanded again, but none of its children is cheaper than what is
already known, so nothing new is added. The result is the same; only a few
expansions are repeated.
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
    reached = {root.state: root}  # state -> the best node found so far
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                heapq.heappush(frontier, (child.path_cost, next(counter), child))
    return None
