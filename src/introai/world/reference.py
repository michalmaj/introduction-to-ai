"""Reference problem formulations over the warehouse world.

These are the course's own versions of what lessons 0.1, 1.3 and 2.4 ask you to write.
Your ``task.py`` must not import this module.
"""

from __future__ import annotations

from collections.abc import Callable

from introai.search.core import Problem
from introai.world.warehouse import Cell, WarehouseMap

State = tuple[Cell, frozenset[Cell]]
_MOVES: dict[str, tuple[int, int]] = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def manhattan(cell: Cell, goal: Cell) -> int:
    """Rows plus columns between two cells (reference for lesson 2.4)."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


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


# --- Heuristics for collecting parcels (lesson 2.7) ------------------------------------


def parcel_heuristic(state: State) -> int:
    """Manhattan distance to the farthest parcel plus the number of parcels left.

    The robot has to drive at least to the farthest parcel, and every parcel takes
    one PICK, so this never overestimates (reference for lesson 2.7).
    """
    cell, parcels = state
    return max((manhattan(cell, parcel) for parcel in parcels), default=0) + len(parcels)


def _parcels_left(state: State) -> int:
    return len(state[1])


def _nearest(state: State) -> int:
    cell, parcels = state
    return min((manhattan(cell, p) for p in parcels), default=0) + len(parcels)


def _sum_of_distances(state: State) -> int:
    cell, parcels = state
    return sum(manhattan(cell, p) for p in parcels) + len(parcels)


def _twice_parcels_left(state: State) -> int:
    return 2 * len(state[1])


CANDIDATE_HEURISTICS: dict[str, Callable[[WarehouseMap], Callable[[State], float]]] = {
    "h1": lambda warehouse: _parcels_left,
    "h2": lambda warehouse: _nearest,
    "h3": lambda warehouse: parcel_heuristic,
    "h4": lambda warehouse: _sum_of_distances,
    "h5": lambda warehouse: lambda state: manhattan(state[0], warehouse.dock),
    "h6": lambda warehouse: _twice_parcels_left,
}
"""The six candidate heuristics of lesson 2.7, Part A, each built for a given map."""

CANDIDATE_ADMISSIBLE: dict[str, bool] = {
    "h1": True,
    "h2": True,
    "h3": True,
    "h4": False,
    "h5": False,
    "h6": False,
}
"""Which of the candidates never overestimate (the answers of lesson 2.7, Part A)."""
