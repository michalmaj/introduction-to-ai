"""Lesson 2.7: designing heuristics.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: decide which of the six candidate heuristics are admissible.
Part B: design your own heuristic for collecting parcels.

Check your work from the repository root:

    uv run pytest modules/02_search/07_designing_heuristics
"""

# ---------------------------------------------------------------------------------------
# Part A: which heuristics are admissible?
# The six candidates h1, ..., h6 are described in the lesson, section "Your turn".
# Replace every None with True (never overestimates) or False.
# ---------------------------------------------------------------------------------------

ADMISSIBLE: dict[str, bool | None] = {
    "h1": None,
    "h2": None,
    "h3": None,
    "h4": None,
    "h5": None,
    "h6": None,
}


# ---------------------------------------------------------------------------------------
# Part B: your heuristic for the parcel pickup problem of lesson 1.3.
#   - a state is (robot cell, frozenset of the parcels still on the floor);
#   - moves and PICK each cost 1;
#   - the heuristic must never overestimate the cost of collecting all parcels, and it
#     must save A* work compared with simply counting the parcels left.
# ---------------------------------------------------------------------------------------


def parcel_heuristic(state: tuple[tuple[int, int], frozenset]) -> float:
    """An admissible estimate of how many actions are needed to collect every parcel."""
    raise NotImplementedError(
        'TODO: implement parcel_heuristic in task.py (or set IMPLEMENTATION = "reference" '
        "in the notebook's first cell)"
    )
