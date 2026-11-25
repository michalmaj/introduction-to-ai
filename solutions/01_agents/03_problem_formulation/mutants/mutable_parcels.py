"""Mutant: keeps the parcels in a mutable set and changes it in place.

Violated requirement: states are immutable and hashable, so a search can remember them.
Common mistake in the lesson: "A mutable set of parcels".
"""

from introai.search import Problem
from introai.world.warehouse import Cell, WarehouseMap

CAUGHT_BY = ("test_states_are_hashable",)

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
        super().__init__((warehouse.start, set(warehouse.parcels)))  # BUG: a mutable set
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
            parcels.discard(cell)  # BUG: changes the old state in place
            return (cell, parcels)
        d_row, d_col = MOVES[action]
        return ((cell[0] + d_row, cell[1] + d_col), parcels)

    def is_goal(self, state: State) -> bool:
        return not state[1]
