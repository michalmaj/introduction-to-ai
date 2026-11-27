"""Mutant: the heuristic only counts the parcels left.

Violated requirement: the heuristic must save A* work compared with counting parcels.
Common mistake in the lesson: "Counting parcels only".
"""

CAUGHT_BY = ("test_heuristic_beats_counting_parcels",)

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
    """One action per parcel left."""
    cell, parcels = state
    return len(parcels)
