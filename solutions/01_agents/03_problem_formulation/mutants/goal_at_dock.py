"""Mutant: treats reaching the dock as the goal.

Violated requirement: the goal is that no parcels are left.
Common mistake in the lesson: "The wrong goal test".
"""

from introai.search import Problem
from introai.world.warehouse import Cell, WarehouseMap

CAUGHT_BY = ("test_is_goal",)

# ---------------------------------------------------------------------------------------
# Part A: 12 free cells (R, D and the parcel cells are free floor too) times 2^3 subsets
# of the 3 parcels.
# ---------------------------------------------------------------------------------------

NUM_STATES: int | None = 96


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------

State = tuple[Cell, frozenset[Cell]]
MOVES = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


class ParcelPickupProblem(Problem):
    """Collect every parcel in the warehouse."""

    def __init__(self, warehouse: WarehouseMap) -> None:
        super().__init__((warehouse.start, frozenset(warehouse.parcels)))
        self.warehouse = warehouse

    def actions(self, state: State) -> list[str]:
        cell, parcels = state
        moves = [
            name
            for name, (d_row, d_col) in MOVES.items()
            if self.warehouse.is_free((cell[0] + d_row, cell[1] + d_col))
        ]
        if cell in parcels:
            moves.append("PICK")
        return moves

    def result(self, state: State, action: str) -> State:
        cell, parcels = state
        if action == "PICK":
            return (cell, parcels - {cell})  # a new frozenset; the old state is untouched
        d_row, d_col = MOVES[action]
        return ((cell[0] + d_row, cell[1] + d_col), parcels)

    def is_goal(self, state: State) -> bool:
        return state[0] == self.warehouse.dock  # BUG: the wrong goal
