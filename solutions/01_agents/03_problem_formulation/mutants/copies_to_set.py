"""Mutant: copies the parcels into a mutable set when picking one up.

The old state stays unchanged, but the new state holds a set, which cannot be put
into another set, so a search cannot remember it.
Violated requirement: states hold a frozenset of parcels.
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
            remaining = set(parcels)  # BUG: a copy, but a mutable set
            remaining.discard(cell)
            return (cell, remaining)
        d_row, d_col = MOVES[action]
        return ((cell[0] + d_row, cell[1] + d_col), parcels)

    def is_goal(self, state: State) -> bool:
        return not state[1]
