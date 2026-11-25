"""Mutant: treats a cell as (x, y) instead of (row, col), so the directions are rotated.

Violated requirement: neighbours in the order N, E, S, W, with N one row up.
Common mistake in the lesson: "Swapping row and column".
"""

from introai.world.warehouse import Cell, WarehouseMap

CAUGHT_BY = ("test_free_neighbours_in_order",)

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
        (row, col - 1),  # BUG: "N" as (x, y - 1)
        (row + 1, col),  # BUG: "E" as (x + 1, y)
        (row, col + 1),  # BUG: "S" as (x, y + 1)
        (row - 1, col),  # BUG: "W" as (x - 1, y)
    ]
    return [c for c in candidates if warehouse.is_free(c)]
