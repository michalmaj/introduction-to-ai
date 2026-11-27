"""Mutant: DFS is believed to find a goal in any state space.

Violated requirement: on an infinite state space DFS can follow an endless branch.
Common mistake in the lesson: "Completeness is the same everywhere".
"""

CAUGHT_BY = ("test_part_a_complete_infinite",)

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
        "complete_infinite": True,
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
