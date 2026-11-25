"""Lesson 2.2: breadth-first and depth-first search.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: trace BFS and DFS by hand on the exercise graph and write your answers below.
Part B: implement bfs() and dfs().

Check your work from the repository root:

    uv run pytest modules/02_search/02_bfs_dfs
"""

from introai.search import Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: trace it by hand.
# The graph and the exact rules are in the lesson, section "Your turn".
# Write each answer as a list of state names, for example ["A", "B", "C"].
# ---------------------------------------------------------------------------------------

# The states in the order BFS expands them, until it finds the goal.
BFS_EXPANSION_ORDER: list[str] | None = None

# The path BFS returns: the states from the start to the goal.
BFS_PATH: list[str] | None = None

# The states in the order DFS expands them, until it finds the goal.
DFS_EXPANSION_ORDER: list[str] | None = None

# The path DFS returns: the states from the start to the goal.
DFS_PATH: list[str] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# Both functions are graph searches:
#   - generate children only with expand(problem, node);
#   - expand every state at most once;
#   - return the goal node (node.states() is then the path), or None if no goal
#     can be reached.
# ---------------------------------------------------------------------------------------


def bfs(problem: Problem) -> Node | None:
    """Breadth-first search: always expand the shallowest node in the frontier."""
    raise NotImplementedError(
        'TODO: implement bfs in task.py (or set IMPLEMENTATION = "reference" in the '
        "notebook's first cell)"
    )


def dfs(problem: Problem) -> Node | None:
    """Depth-first search: always expand the deepest node in the frontier."""
    raise NotImplementedError(
        'TODO: implement dfs in task.py (or set IMPLEMENTATION = "reference" in the '
        "notebook's first cell)"
    )
