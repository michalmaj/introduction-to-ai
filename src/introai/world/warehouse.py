"""The warehouse: a grid of shelves and aisles that the delivery robot moves in.

Maps are plain text files you can edit yourself::

    #######
    #R..#.#
    #.#...#
    #...#D#
    #######

``#`` is an obstacle (wall or shelf), ``.`` is free floor, ``R`` is where the
robot starts and ``D`` is the dock it has to reach. A map must be rectangular
and contain exactly one ``R`` and one ``D``.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from introai.search.core import Problem

Cell = tuple[int, int]
"""A grid cell as ``(row, col)``, counted from 0 at the top-left corner."""

_ALLOWED = {"#", ".", "R", "D"}
_MOVES: dict[str, tuple[int, int]] = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


@dataclass(frozen=True)
class WarehouseMap:
    """A rectangular warehouse map."""

    rows: int
    cols: int
    walls: frozenset[Cell]
    start: Cell
    dock: Cell

    @classmethod
    def from_text(cls, text: str) -> WarehouseMap:
        """Parse a map; tolerates a BOM, CRLF line endings and trailing whitespace."""
        numbered = [(n, line.rstrip()) for n, line in enumerate(text.lstrip("﻿").splitlines(), 1)]
        while numbered and not numbered[0][1]:
            numbered.pop(0)
        while numbered and not numbered[-1][1]:
            numbered.pop()
        if not numbered:
            raise ValueError("map is empty")

        cols = len(numbered[0][1])
        walls: set[Cell] = set()
        found: dict[str, list[Cell]] = {"R": [], "D": []}
        for row, (line_no, line) in enumerate(numbered):
            if len(line) != cols:
                raise ValueError(f"line {line_no} has {len(line)} characters, expected {cols}")
            for col, char in enumerate(line):
                if char not in _ALLOWED:
                    raise ValueError(
                        f"unknown character {char!r} at line {line_no}, column {col + 1}"
                    )
                if char == "#":
                    walls.add((row, col))
                elif char in found:
                    found[char].append((row, col))

        for marker in ("R", "D"):
            if len(found[marker]) != 1:
                raise ValueError(
                    f"map must contain exactly one {marker!r} (found {len(found[marker])})"
                )

        return cls(len(numbered), cols, frozenset(walls), found["R"][0], found["D"][0])

    @classmethod
    def from_file(cls, path: str | Path) -> WarehouseMap:
        """Read a map from a text file (UTF-8, with or without a BOM)."""
        try:
            text = Path(path).read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError(
                f"cannot read {path}: save the map as UTF-8 text (not UTF-16 or another encoding)"
            ) from None
        return cls.from_text(text)

    def is_free(self, cell: Cell) -> bool:
        """Whether the robot may stand on ``cell``."""
        row, col = cell
        return 0 <= row < self.rows and 0 <= col < self.cols and cell not in self.walls


class RouteProblem(Problem):
    """Drive the robot from ``R`` to ``D``; every move costs 1.

    States are cells; actions are compass moves ``"N"``, ``"E"``, ``"S"``, ``"W"``,
    tried in ``action_order``.
    """

    def __init__(
        self, warehouse: WarehouseMap, action_order: Sequence[str] = ("N", "E", "S", "W")
    ) -> None:
        super().__init__(warehouse.start)
        self.warehouse = warehouse
        self.action_order = tuple(action_order)

    def actions(self, state: Cell) -> list[str]:
        return [a for a in self.action_order if self.warehouse.is_free(_move(state, a))]

    def result(self, state: Cell, action: str) -> Cell:
        target = _move(state, action)
        if not self.warehouse.is_free(target):
            raise ValueError(f"cannot move {action} from {state}: the way is blocked")
        return target

    def is_goal(self, state: Cell) -> bool:
        return state == self.warehouse.dock


def _move(cell: Cell, action: str) -> Cell:
    d_row, d_col = _MOVES[action]
    return (cell[0] + d_row, cell[1] + d_col)


def render_text(
    warehouse: WarehouseMap, path: Sequence[Cell] = (), expanded: Iterable[Cell] = ()
) -> str:
    """Draw the map as text: ``*`` marks the path, ``o`` other expanded cells."""
    grid = [
        ["#" if (row, col) in warehouse.walls else "." for col in range(warehouse.cols)]
        for row in range(warehouse.rows)
    ]
    for row, col in expanded:
        grid[row][col] = "o"
    for row, col in path:
        grid[row][col] = "*"
    grid[warehouse.start[0]][warehouse.start[1]] = "R"
    grid[warehouse.dock[0]][warehouse.dock[1]] = "D"
    return "\n".join("".join(line) for line in grid)
