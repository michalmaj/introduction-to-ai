"""Lesson 0.1: setup and how to use the course.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: read two positions off the map data/maps/small.txt.
Part B: implement free_neighbours().

Check your work from the repository root:

    uv run pytest modules/00_start/01_setup
"""

from introai.world.warehouse import Cell, WarehouseMap

# ---------------------------------------------------------------------------------------
# Part A: read the map data/maps/small.txt.
# Write each position as a pair (row, col), for example (2, 4).
# ---------------------------------------------------------------------------------------

# Where the robot starts (the cell marked R).
START: tuple[int, int] | None = None

# Where the dock is (the cell marked D).
DOCK: tuple[int, int] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def free_neighbours(warehouse: WarehouseMap, cell: Cell) -> list[Cell]:
    """The free cells next to ``cell``, in the order N, E, S, W.

    North is one row up, east one column to the right, south one row down and west
    one column to the left. Use ``warehouse.is_free(c)`` to decide whether the robot
    may stand on a cell ``c``.
    """
    raise NotImplementedError(
        'TODO: implement free_neighbours in task.py (or set IMPLEMENTATION = "reference" '
        "in the notebook's first cell)"
    )
