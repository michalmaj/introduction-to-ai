"""Mutant: returns every neighbouring cell, obstacles included.

Violated requirement: only cells the robot may stand on are free neighbours.
Common mistake in the lesson: "Forgetting the obstacles".
"""

from introai.world.warehouse import Cell, WarehouseMap

CAUGHT_BY = ("test_free_neighbours_skips_obstacles",)

# ---------------------------------------------------------------------------------------
# Part A: positions on data/maps/small.txt.
# ---------------------------------------------------------------------------------------

START: tuple[int, int] | None = (1, 1)
DOCK: tuple[int, int] | None = (3, 5)


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def free_neighbours(warehouse: WarehouseMap, cell: Cell) -> list[Cell]:
    """The free cells next to ``cell``, in the order N, E, S, W."""
    row, col = cell
    candidates = [
        (row - 1, col),  # N: one row up
        (row, col + 1),  # E: one column right
        (row + 1, col),  # S: one row down
        (row, col - 1),  # W: one column left
    ]
    return candidates  # BUG: no check at all
