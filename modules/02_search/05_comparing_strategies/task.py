"""Lesson 2.5: comparing search strategies.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: fill in the table of properties below.
This lesson has no Part B: the notebook compares the algorithms you wrote in
lessons 2.2–2.4 (or the course's reference versions).

Check your work from the repository root:

    uv run pytest modules/02_search/05_comparing_strategies
"""

# ---------------------------------------------------------------------------------------
# Part A: the properties of the five strategies.
# Replace every None with True or False. The exact meaning of each property, with all
# its assumptions, is in the lesson, section "Properties to compare".
# ---------------------------------------------------------------------------------------

PROPERTIES: dict[str, dict[str, bool | None]] = {
    "BFS": {
        "complete_finite": None,
        "complete_infinite": None,
        "optimal_unit_costs": None,
        "optimal_any_costs": None,
    },
    "DFS": {
        "complete_finite": None,
        "complete_infinite": None,
        "optimal_unit_costs": None,
        "optimal_any_costs": None,
    },
    "UCS": {
        "complete_finite": None,
        "complete_infinite": None,
        "optimal_unit_costs": None,
        "optimal_any_costs": None,
    },
    "greedy": {
        "complete_finite": None,
        "complete_infinite": None,
        "optimal_unit_costs": None,
        "optimal_any_costs": None,
    },
    "A*": {
        "complete_finite": None,
        "complete_infinite": None,
        "optimal_unit_costs": None,
        "optimal_any_costs": None,
    },
}
