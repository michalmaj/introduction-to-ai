"""Mutant: depth-limited search returns None when it was cut off at the limit.

Violated requirement: a cutoff (CUTOFF) is different from "no goal at all" (None);
iterative deepening must go deeper after a cutoff.
Common mistake in the lesson: "A cutoff reported as failure".
"""

from introai.search import CUTOFF, Node, Problem, expand

CAUGHT_BY = ("test_dls_reports_cutoff", "test_ids_finds_a_shortest_path")

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise graph.
# ---------------------------------------------------------------------------------------

IDS_EXPANSIONS_PER_ITERATION: list[int] | None = [0, 1, 3, 7]


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def depth_limited_search(problem: Problem, limit: int) -> Node | str | None:
    """Depth-first search that never expands a node at depth ``limit`` or deeper."""
    frontier = [Node(problem.initial)]
    result = None
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        if node.depth >= limit:
            pass  # the cutoff is forgotten
        elif not is_cycle(node):
            frontier.extend(reversed(expand(problem, node)))
    return result


def iterative_deepening_search(problem: Problem) -> Node | None:
    """Depth-limited search with the limits 0, 1, 2, ... until the result is not CUTOFF."""
    limit = 0
    while True:
        result = depth_limited_search(problem, limit)
        if result != CUTOFF:
            return result
        limit += 1


def is_cycle(node: Node) -> bool:
    """Whether the node's state already appears among its ancestors."""
    ancestor = node.parent
    while ancestor is not None:
        if ancestor.state == node.state:
            return True
        ancestor = ancestor.parent
    return False
