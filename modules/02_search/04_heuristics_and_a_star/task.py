"""Lesson 2.4: heuristics, greedy best-first search and A*.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: trace greedy best-first search and A* by hand and write your answers below.
Part B: implement manhattan(), greedy_best_first() and a_star().

Check your work from the repository root:

    uv run pytest modules/02_search/04_heuristics_and_a_star
"""

from collections.abc import Callable

from introai.search import Node, Problem, expand

# ---------------------------------------------------------------------------------------
# Part A: trace it by hand.
# The graph, its heuristic and the exact rules are in the lesson, section "Your turn".
# Write each answer as a list of state names, for example ["A", "B", "C"].
# ---------------------------------------------------------------------------------------

# The path greedy best-first search returns: the states from the start to the goal.
GREEDY_PATH: list[str] | None = None

# The states in the order A* expands them, until it removes the goal from the frontier.
# Skipped (out-of-date) frontier entries are not expansions.
ASTAR_EXPANSION_ORDER: list[str] | None = None

# The path A* returns: the states from the start to the goal.
ASTAR_PATH: list[str] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - manhattan: the number of rows plus the number of columns between two cells;
#   - greedy_best_first and a_star are best-first searches like your ucs from lesson 2.3,
#     with a different priority: h(state) for greedy, path cost + h(state) for A*;
#   - generate children only with expand(problem, node);
#   - test for the goal when a node is removed from the frontier;
#   - return the goal node, or None if no goal can be reached.
# ---------------------------------------------------------------------------------------


def manhattan(cell: tuple[int, int], goal: tuple[int, int]) -> int:
    """The Manhattan distance between two cells given as (row, col)."""
    raise NotImplementedError(
        'TODO: implement manhattan in task.py (or set IMPLEMENTATION = "reference" in the '
        "notebook's first cell)"
    )


def greedy_best_first(problem: Problem, h: Callable) -> Node | None:
    """Greedy best-first search: always expand the node whose state has the lowest h."""
    raise NotImplementedError(
        'TODO: implement greedy_best_first in task.py (or set IMPLEMENTATION = "reference" '
        "in the notebook's first cell)"
    )


def a_star(problem: Problem, h: Callable) -> Node | None:
    """A* search: always expand the node with the lowest f = path cost + h(state)."""
    raise NotImplementedError(
        'TODO: implement a_star in task.py (or set IMPLEMENTATION = "reference" in the '
        "notebook's first cell)"
    )
