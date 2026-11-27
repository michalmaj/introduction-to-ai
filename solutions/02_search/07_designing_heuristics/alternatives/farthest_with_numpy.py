"""Alternative: the reference heuristic written with numpy.

It returns numpy numbers (np.int64), which are numbers like any other.
"""

import numpy as np

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


def parcel_heuristic(state: tuple[tuple[int, int], frozenset]) -> float:
    """The farthest parcel plus the picks, with the distances computed by numpy."""
    cell, parcels = state
    if not parcels:
        return 0
    distances = np.abs(np.array(sorted(parcels)) - np.array(cell)).sum(axis=1)
    return distances.max() + len(parcels)
