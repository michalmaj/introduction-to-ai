"""Reference problem formulations over the warehouse world.

These are the course's own versions of what lessons 0.1 and 1.3 ask you to write.
Your ``task.py`` must not import this module.
"""

from __future__ import annotations

from introai.search.core import Problem
from introai.world.warehouse import Cell, WarehouseMap

State = tuple[Cell, frozenset[Cell]]
_MOVES: dict[str, tuple[int, int]] = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def free_neighbours(warehouse: WarehouseMap, cell: Cell) -> list[Cell]:
    """The free cells next to ``cell``, in the order N, E, S, W (reference for lesson 0.1)."""
    neighbours = [(cell[0] + d_row, cell[1] + d_col) for d_row, d_col in _MOVES.values()]
    return [n for n in neighbours if warehouse.is_free(n)]


class ParcelPickupProblem(Problem):
    """Collect every parcel: the full state of the parcel world as a search problem.

    - state: ``(robot cell, frozenset of the parcels still lying on the floor)``;
    - actions: the moves N, E, S, W into free cells, then ``"PICK"`` if a parcel
      lies on the robot's cell;
    - ``PICK`` removes that parcel; a move changes only the robot's cell;
    - goal: no parcels left; every action costs 1.
    """

    def __init__(self, warehouse: WarehouseMap) -> None:
        super().__init__((warehouse.start, warehouse.parcels))
        self.warehouse = warehouse

    def _target(self, cell: Cell, action: str) -> Cell:
        d_row, d_col = _MOVES[action]
        return (cell[0] + d_row, cell[1] + d_col)

    def actions(self, state: State) -> list[str]:
        cell, parcels = state
        moves = [a for a in _MOVES if self.warehouse.is_free(self._target(cell, a))]
        return moves + (["PICK"] if cell in parcels else [])

    def result(self, state: State, action: str) -> State:
        if action not in self.actions(state):
            raise ValueError(f"{action!r} is not possible in state {state}")
        cell, parcels = state
        if action == "PICK":
            return (cell, parcels - {cell})
        return (self._target(cell, action), parcels)

    def is_goal(self, state: State) -> bool:
        return not state[1]
