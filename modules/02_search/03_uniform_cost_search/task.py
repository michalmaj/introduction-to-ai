"""Lesson 2.3: uniform-cost search.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: trace UCS by hand on the weighted exercise graph and write your answers below.
Part B: implement ucs().

Check your work from the repository root:

    uv run pytest modules/02_search/03_uniform_cost_search
"""

from introai.search import Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: trace it by hand.
# The graph and the exact rules are in the lesson, section "Your turn".
# Write each answer as a list of state names, for example ["A", "B", "C"].
# ---------------------------------------------------------------------------------------

# The states in the order UCS expands them, until it removes the goal from the frontier.
# Skipped (out-of-date) frontier entries are not expansions.
UCS_EXPANSION_ORDER: list[str] | None = None

# The path UCS returns: the states from the start to the goal.
UCS_PATH: list[str] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - the frontier is a priority queue ordered by path cost (use heapq);
#   - generate children only with expand(problem, node);
#   - test for the goal when a node is removed from the frontier, not when it is generated;
#   - return the goal node (node.states() is then the path), or None if no goal can be
#     reached.
# ---------------------------------------------------------------------------------------


def ucs(problem: Problem) -> Node | None:
    """Uniform-cost search: always expand the node with the lowest path cost."""
    raise NotImplementedError(
        'TODO: implement ucs in task.py (or set IMPLEMENTATION = "reference" in the '
        "notebook's first cell)"
    )
