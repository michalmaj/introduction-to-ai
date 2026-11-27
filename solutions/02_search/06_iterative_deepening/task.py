"""Lesson 2.6: depth-limited search and iterative deepening (reference solution).

Do not read this before you have tried the lesson yourself.
"""

from introai.search import CUTOFF, Node, Problem, expand

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
            result = CUTOFF  # there may be a goal deeper down
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
