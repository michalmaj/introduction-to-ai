"""Alternative: recursive depth-limited search, as in the third edition of Russell and Norvig."""

from introai.search import CUTOFF, Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise graph.
# ---------------------------------------------------------------------------------------

IDS_EXPANSIONS_PER_ITERATION: list[int] | None = [0, 1, 3, 7]


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def depth_limited_search(problem: Problem, limit: int) -> Node | str | None:
    """Recursive depth-limited search: the call stack plays the role of the frontier."""
    return recursive_dls(problem, Node(problem.initial), limit)


def recursive_dls(problem: Problem, node: Node, limit: int) -> Node | str | None:
    if problem.is_goal(node.state):
        return node
    if node.depth >= limit:
        return CUTOFF
    if is_cycle(node):
        return None
    cutoff = False
    for child in expand(problem, node):
        result = recursive_dls(problem, child, limit)
        if result == CUTOFF:
            cutoff = True
        elif result is not None:
            return result
    return CUTOFF if cutoff else None


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
