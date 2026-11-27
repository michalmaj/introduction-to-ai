"""Mutant: greedy best-first search is believed to find the cheapest route.

Violated requirement: greedy follows the heuristic alone and ignores the cost so far.
Common mistake in the lesson: "Greedy heads straight for the goal, so it is optimal".
"""

CAUGHT_BY = ("test_part_a_optimal_unit_costs",)

# ---------------------------------------------------------------------------------------
# Part A: the properties of the five strategies.
# Replace every None with True or False. The exact meaning of each property, with all
# its assumptions, is in the lesson, section "Properties to compare".
# ---------------------------------------------------------------------------------------

PROPERTIES: dict[str, dict[str, bool | None]] = {
    "BFS": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": False,
    },
    "DFS": {
        "complete_finite": True,
        "complete_infinite": False,
        "optimal_unit_costs": False,
        "optimal_any_costs": False,
    },
    "UCS": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": True,
    },
    "greedy": {
        "complete_finite": True,
        "complete_infinite": False,
        "optimal_unit_costs": True,
        "optimal_any_costs": False,
    },
    "A*": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": True,
    },
}
