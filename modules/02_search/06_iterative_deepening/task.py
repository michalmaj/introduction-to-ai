"""Lesson 2.6: depth-limited search and iterative deepening.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: count the expansions of iterative deepening by hand and write them below.
Part B: implement depth_limited_search() and iterative_deepening_search().

Check your work from the repository root:

    uv run pytest modules/02_search/06_iterative_deepening
"""

from introai.search import CUTOFF, Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: count it by hand.
# The graph and the exact rules are in the lesson, section "Your turn".
# ---------------------------------------------------------------------------------------

# How many nodes depth-limited search expands with the limits 0, 1, 2, ..., until
# iterative deepening finds the goal. For example [0, 1, 2] for three iterations.
IDS_EXPANSIONS_PER_ITERATION: list[int] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - generate children only with expand(problem, node);
#   - depth_limited_search returns the goal node, CUTOFF if some node was cut off at the
#     limit, or None if there is no goal at all;
#   - a node whose state already appears on its path is a cycle: do not expand it.
# ---------------------------------------------------------------------------------------


def depth_limited_search(problem: Problem, limit: int) -> Node | str | None:
    """Depth-first search that never expands a node at depth ``limit`` or deeper."""
    raise NotImplementedError(
        "TODO: implement depth_limited_search in task.py (or set IMPLEMENTATION = "
        '"reference" in the notebook\'s first cell)'
    )


def iterative_deepening_search(problem: Problem) -> Node | None:
    """Depth-limited search with the limits 0, 1, 2, ... until the result is not CUTOFF."""
    raise NotImplementedError(
        "TODO: implement iterative_deepening_search in task.py (or set IMPLEMENTATION = "
        '"reference" in the notebook\'s first cell)'
    )
