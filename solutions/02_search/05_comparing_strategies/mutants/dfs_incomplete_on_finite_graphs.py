"""Mutant: DFS is believed to loop forever even on a finite graph.

Violated requirement: a graph search that remembers expanded states stops on every
finite state space.
Common mistake in the lesson: "Confusing DFS with tree search".
"""

CAUGHT_BY = ("test_part_a_complete_finite",)

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
        "complete_finite": False,
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
