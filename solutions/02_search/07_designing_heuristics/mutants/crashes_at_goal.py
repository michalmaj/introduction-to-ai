"""Mutant: the heuristic takes max() over the parcels even when none are left.

Violated requirement: a heuristic is defined in every state, including the goal,
where it must be 0.
Common mistake in the lesson: "No case for zero parcels".
"""

CAUGHT_BY = ("test_heuristic_is_zero_at_goal_states",)

# ---------------------------------------------------------------------------------------
# Part A: answers.
# ---------------------------------------------------------------------------------------

ADMISSIBLE: dict[str, bool | None] = {
    "h1": True,
    "h2": True,
    "h3": True,
    "h4": False,
    "h5": False,
    "h6": False,
}


# ---------------------------------------------------------------------------------------
# Part B: the farthest parcel plus one PICK per parcel.
# ---------------------------------------------------------------------------------------


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parcel_heuristic(state: tuple[tuple[int, int], frozenset]) -> float:
    """The robot drives at least to the farthest parcel and picks each parcel once."""
    cell, parcels = state
    return max(manhattan(cell, parcel) for parcel in parcels) + len(parcels)
