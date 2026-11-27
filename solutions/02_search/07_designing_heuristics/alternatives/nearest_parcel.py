"""Alternative: the distance to the nearest parcel plus one PICK per parcel.

Admissible (the robot has to reach some parcel first), but weaker than the farthest
parcel: the reference heuristic dominates it, so A* expands more nodes with it.
"""

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
    """The robot reaches some parcel first and picks each parcel once."""
    cell, parcels = state
    if not parcels:
        return 0
    return min(manhattan(cell, parcel) for parcel in parcels) + len(parcels)
