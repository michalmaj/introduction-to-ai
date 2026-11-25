"""Mutant: checks only for walls, so on a map without border walls it returns cells
outside the map.

Violated requirement: a free neighbour lies on the map.
Common mistake in the lesson: "Walking off the edge of the map".
"""

from introai.world.warehouse import Cell, WarehouseMap

CAUGHT_BY = ("test_free_neighbours_never_leaves_the_map",)

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
    return [c for c in candidates if c not in warehouse.walls]  # BUG: ignores the edges
