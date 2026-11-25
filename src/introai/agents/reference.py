"""Reference agents for the parcel world, and the answers to lesson 1.2's Part A.

Your ``task.py`` must not import this module.
"""

from __future__ import annotations

from introai.agents.world import Percept

_MOVES: dict[str, tuple[int, int]] = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def reflex_agent(percept: Percept) -> str:
    """A simple reflex agent: condition-action rules on the current percept only.

    1. A parcel here: pick it up.
    2. Otherwise: move in the first free direction, in the order N, E, S, W.
    3. Nowhere to go: wait.
    """
    if percept.parcel_here:
        return "PICK"
    if percept.free:
        return percept.free[0]
    return "WAIT"


class ModelBasedAgent:
    """A model-based agent: it remembers where it has been.

    It cannot see its position, but it can work it out: a move in a free
    direction always succeeds, so it tracks its position relative to the start
    (dead reckoning) and counts how often it has visited each cell. It prefers
    the free neighbour it has visited least (ties broken N, E, S, W).
    """

    def __init__(self) -> None:
        self.position = (0, 0)
        self.visits: dict[tuple[int, int], int] = {self.position: 1}

    def __call__(self, percept: Percept) -> str:
        if percept.parcel_here:
            return "PICK"
        if not percept.free:
            return "WAIT"

        def neighbour(direction: str) -> tuple[int, int]:
            d_row, d_col = _MOVES[direction]
            return (self.position[0] + d_row, self.position[1] + d_col)

        direction = min(percept.free, key=lambda d: self.visits.get(neighbour(d), 0))
        self.position = neighbour(direction)
        self.visits[self.position] = self.visits.get(self.position, 0) + 1
        return direction


# Part A of lesson 1.2: the properties of the two environment variants described there.
ENVIRONMENT_PROPERTIES: dict[str, dict[str, str]] = {
    "variant_1": {
        "observable": "partially",
        "agents": "single",
        "deterministic": "deterministic",
        "episodic": "sequential",
        "static": "static",
        "discrete": "discrete",
    },
    "variant_2": {
        "observable": "fully",
        "agents": "multi",
        "deterministic": "stochastic",
        "episodic": "sequential",
        "static": "dynamic",
        "discrete": "discrete",
    },
}
