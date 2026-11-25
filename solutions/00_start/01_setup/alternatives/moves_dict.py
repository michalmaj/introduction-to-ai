"""Alternative: the four directions as a dictionary of row and column offsets."""

from introai.world.warehouse import Cell, WarehouseMap

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
    moves = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
    result = []
    for d_row, d_col in moves.values():
        neighbour = (cell[0] + d_row, cell[1] + d_col)
        if warehouse.is_free(neighbour):
            result.append(neighbour)
    return result
