"""Lesson 2.1: state spaces and search trees.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: count the nodes of a search tree by hand and write your answers below.
Part B: implement expand() and count_tree_nodes().

Check your work from the repository root:

    uv run pytest modules/02_search/01_state_space
"""

from introai.search import Node, Problem

# ---------------------------------------------------------------------------------------
# Part A: count it by hand.
# The graph and the exact rules are in the lesson, section "Your turn".
# Write each answer as a whole number, for example 7.
# ---------------------------------------------------------------------------------------

# How many nodes the search tree of the exercise graph has at depth 2.
TREE_NODES_AT_DEPTH_2: int | None = None

# How many different states those depth-2 nodes hold.
STATES_AT_DEPTH_2: int | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - expand: write it yourself, without the course's expand from introai.search;
#   - count_tree_nodes: build the tree level by level with your expand, keeping every
#     node (no set of reached states) and never testing for the goal.
# ---------------------------------------------------------------------------------------


def expand(problem: Problem, node: Node) -> list[Node]:
    """The children of ``node``: one per action, in the order of ``problem.actions``.

    Each child knows its parent (``node``), the action that led to it, the cost of
    the whole path from the root (``path_cost``) and its depth.
    """
    raise NotImplementedError(
        'TODO: implement expand in task.py (or set IMPLEMENTATION = "reference" in the '
        "notebook's first cell)"
    )


def count_tree_nodes(problem: Problem, depth: int) -> list[int]:
    """The number of search tree nodes at each depth 0, 1, ..., ``depth``.

    The tree starts with one root node for ``problem.initial``. It keeps every path,
    even one that comes back to a state already in the tree.
    """
    raise NotImplementedError(
        'TODO: implement count_tree_nodes in task.py (or set IMPLEMENTATION = "reference" '
        "in the notebook's first cell)"
    )
