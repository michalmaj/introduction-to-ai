"""Mutant: the distance to the nearest parcel is multiplied by the number of parcels.

Violated requirement: an admissible heuristic never overestimates; when the parcels lie
close together, the robot does not have to drive that far for each of them.
Common mistake in the lesson: "Multiplying by the number of parcels".
"""

CAUGHT_BY = ("test_heuristic_is_admissible",)

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
    """The nearest parcel's distance, once per parcel, plus the picks."""
    cell, parcels = state
    if not parcels:
        return 0
    return min(manhattan(cell, parcel) for parcel in parcels) * len(parcels) + len(parcels)
