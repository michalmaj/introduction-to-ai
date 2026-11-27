"""Mutant: BFS is believed to find the cheapest route whatever the step costs.

Violated requirement: BFS minimises the number of steps, not the cost.
Common mistake in the lesson: "Confusing steps with cost".
"""

CAUGHT_BY = ("test_part_a_optimal_any_costs",)

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
        "optimal_any_costs": True,
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
        "optimal_unit_costs": False,
        "optimal_any_costs": False,
    },
    "A*": {
        "complete_finite": True,
        "complete_infinite": True,
        "optimal_unit_costs": True,
        "optimal_any_costs": True,
    },
}
