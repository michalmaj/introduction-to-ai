"""Alternative: drive to the nearest parcel, then at least across the parcels' spread.

Whatever the order, the robot first reaches some parcel (at least the nearest one
away), and afterwards it must visit both parcels of the farthest-apart pair, which
takes at least their distance. Both parts are lower bounds, so their sum is too.
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
    """Nearest parcel, plus the largest distance between two parcels, plus the picks."""
    cell, parcels = state
    if not parcels:
        return 0
    nearest = min(manhattan(cell, parcel) for parcel in parcels)
    spread = max(manhattan(p, q) for p in parcels for q in parcels)
    return nearest + spread + len(parcels)
