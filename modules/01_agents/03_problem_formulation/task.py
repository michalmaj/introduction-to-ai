"""Lesson 1.3: agent types and problem formulation.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: count the states of the problem on data/maps/parcels.txt.
Part B: implement the ParcelPickupProblem class.

Check your work from the repository root:

    uv run pytest modules/01_agents/03_problem_formulation
"""

from introai.search import Problem
from introai.world.warehouse import Cell, WarehouseMap

# ---------------------------------------------------------------------------------------
# Part A: how many states does the problem have on data/maps/parcels.txt?
# Count every combination of a free robot cell and a set of parcels still on the floor.
# ---------------------------------------------------------------------------------------

NUM_STATES: int | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation (the exact specification is in the lesson, section "Task").
# ---------------------------------------------------------------------------------------

State = tuple[Cell, frozenset[Cell]]


class ParcelPickupProblem(Problem):
    """Collect every parcel in the warehouse.

    - state: (robot cell, frozenset of the parcels still lying on the floor);
    - actions: moves "N", "E", "S", "W" into free cells, and "PICK" when a parcel
      lies on the robot's cell;
    - goal: no parcels left; every action costs 1 (inherited from Problem).
    """

    def __init__(self, warehouse: WarehouseMap) -> None:
        raise NotImplementedError(
            "TODO: implement ParcelPickupProblem.__init__ in task.py "
            '(or set IMPLEMENTATION = "reference" in the notebook\'s first cell)'
        )

    def actions(self, state: State) -> list[str]:
        raise NotImplementedError(
            "TODO: implement ParcelPickupProblem.actions in task.py "
            '(or set IMPLEMENTATION = "reference" in the notebook\'s first cell)'
        )

    def result(self, state: State, action: str) -> State:
        raise NotImplementedError(
            "TODO: implement ParcelPickupProblem.result in task.py "
            '(or set IMPLEMENTATION = "reference" in the notebook\'s first cell)'
        )

    def is_goal(self, state: State) -> bool:
        raise NotImplementedError(
            "TODO: implement ParcelPickupProblem.is_goal in task.py "
            '(or set IMPLEMENTATION = "reference" in the notebook\'s first cell)'
        )
