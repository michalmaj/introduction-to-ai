"""Mutant: the heuristic adds up the distances to all parcels.

Violated requirement: an admissible heuristic never overestimates; one drive can
pass several parcels, so the sum counts some of the way more than once.
Common mistake in the lesson: "Counting the same drive twice".
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
    """The distances to all parcels added up, plus the picks."""
    cell, parcels = state
    return sum(manhattan(cell, parcel) for parcel in parcels) + len(parcels)
