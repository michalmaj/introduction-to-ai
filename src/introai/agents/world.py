"""The parcel world: a robot collects parcels in the warehouse.

The robot does not see the whole map. Each step it receives a :class:`Percept`:
whether a parcel lies on its own cell and which of the four directions are free.
It answers with one action:

- ``"N"``, ``"E"``, ``"S"``, ``"W"`` move one cell; a move into an obstacle (or
  off the map) does nothing, the robot just bumps;
- ``"PICK"`` picks up a parcel lying on the robot's cell (otherwise nothing);
- ``"WAIT"`` does nothing.

Performance measure: every action costs 1 point; every parcel collected earns 10.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from introai.world.warehouse import Cell, WarehouseMap

ACTIONS: tuple[str, ...] = ("N", "E", "S", "W", "PICK", "WAIT")
_MOVES: dict[str, tuple[int, int]] = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
PARCEL_REWARD = 10
ACTION_COST = 1


@dataclass(frozen=True)
class Percept:
    """What the robot senses: a parcel on its cell, and the free directions (N, E, S, W order)."""

    parcel_here: bool
    free: tuple[str, ...]


class ParcelWorld:
    """The environment: it keeps the true state and scores the robot's actions."""

    def __init__(self, warehouse: WarehouseMap) -> None:
        self.warehouse = warehouse
        self.robot: Cell = warehouse.start
        self.parcels: set[Cell] = set(warehouse.parcels)
        self.score = 0
        self.steps = 0
        self.collected = 0

    @property
    def done(self) -> bool:
        """Whether every parcel has been collected."""
        return not self.parcels

    def percept(self) -> Percept:
        free = tuple(
            direction
            for direction, (d_row, d_col) in _MOVES.items()
            if self.warehouse.is_free((self.robot[0] + d_row, self.robot[1] + d_col))
        )
        return Percept(self.robot in self.parcels, free)

    def step(self, action: str) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown action {action!r}; expected one of {', '.join(ACTIONS)}")
        self.steps += 1
        self.score -= ACTION_COST
        if action in _MOVES:
            d_row, d_col = _MOVES[action]
            target = (self.robot[0] + d_row, self.robot[1] + d_col)
            if self.warehouse.is_free(target):
                self.robot = target
        elif action == "PICK" and self.robot in self.parcels:
            self.parcels.remove(self.robot)
            self.collected += 1
            self.score += PARCEL_REWARD


@dataclass(frozen=True)
class EpisodeResult:
    score: float
    steps: int
    collected: int
    trajectory: tuple[Cell, ...]


def run_episode(
    agent: Callable[[Percept], str], warehouse: WarehouseMap, max_steps: int = 200
) -> EpisodeResult:
    """Let ``agent`` act in a fresh world until every parcel is collected or time runs out."""
    world = ParcelWorld(warehouse)
    trajectory = [world.robot]
    while not world.done and world.steps < max_steps:
        world.step(agent(world.percept()))
        trajectory.append(world.robot)
    return EpisodeResult(world.score, world.steps, world.collected, tuple(trajectory))


def random_agent(seed: int = 0) -> Callable[[Percept], str]:
    """An agent that ignores its percept and picks a random action (a baseline)."""
    rng = random.Random(seed)

    def agent(percept: Percept) -> str:
        return rng.choice(ACTIONS)

    return agent
