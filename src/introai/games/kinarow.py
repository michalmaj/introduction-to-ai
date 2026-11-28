"""Tic-tac-toe and its bigger relatives: k marks in a row on an m × n board.

A state is a tuple of row strings, for example ``("X..", ".O.", "...")``. X moves
first, so the player to move follows from the numbers of marks. A move is the
``(row, col)`` of an empty cell. The game ends when a player has ``k`` marks in
a row (horizontally, vertically or diagonally) or the board is full.
"""

from __future__ import annotations

from collections.abc import Sequence

from introai.games.core import Game
from introai.trace import emit

Cell = tuple[int, int]
Board = tuple[str, ...]

EMPTY = "."
_MARKS = frozenset("XO.")


class KInARow(Game):
    """The game of ``k`` in a row on an ``m`` × ``n`` board, without gravity."""

    players = ("X", "O")

    def __init__(self, m: int = 3, n: int = 3, k: int = 3) -> None:
        if m < 1 or n < 1 or k < 1 or k > max(m, n):
            raise ValueError(f"no line of {k} fits on a {m} × {n} board")
        self.m, self.n, self.k = m, n, k
        self.initial: Board = (EMPTY * n,) * m
        lines = []
        for r in range(m):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    cells = tuple((r + i * dr, c + i * dc) for i in range(k))
                    if all(0 <= rr < m and 0 <= cc < n for rr, cc in cells):
                        lines.append(cells)
        self.lines: tuple[tuple[Cell, ...], ...] = tuple(lines)
        """Every row of ``k`` cells that wins: rows, columns and both diagonals."""

    def __repr__(self) -> str:
        return f"KInARow({self.m}, {self.n}, {self.k})"

    def from_rows(self, rows: Sequence[str]) -> Board:
        """Check a board written as rows, e.g. ``["X..", ".O.", "..."]``, and return it."""
        if isinstance(rows, str) or len(rows) != self.m:
            raise ValueError(f"a board of this game has {self.m} rows, given as a list of strings")
        for row in rows:
            if not isinstance(row, str) or len(row) != self.n or not set(row) <= _MARKS:
                raise ValueError(
                    f"every row has {self.n} characters, each 'X', 'O' or '.': got {row!r}"
                )
        x = sum(row.count("X") for row in rows)
        o = sum(row.count("O") for row in rows)
        if x - o not in (0, 1):
            raise ValueError(f"X moves first, so X has as many marks as O or one more ({x}, {o})")
        return tuple(rows)

    def render(self, state: Board) -> str:
        """The board as text, one row per line."""
        return "\n".join(state)

    def to_move(self, state: Board) -> str:
        x = sum(row.count("X") for row in state)
        o = sum(row.count("O") for row in state)
        return "X" if x == o else "O"

    def actions(self, state: Board) -> list[Cell]:
        """The empty cells, row by row, left to right."""
        return [(r, c) for r, row in enumerate(state) for c, mark in enumerate(row) if mark == "."]

    def result(self, state: Board, action: Cell) -> Board:
        emit("result", state=state, action=action)
        try:
            r, c = action
            valid = 0 <= r < self.m and 0 <= c < self.n and state[r][c] == EMPTY
        except (TypeError, ValueError):
            valid = False
        if not valid:
            raise ValueError(f"{action!r} is not an empty cell (row, col) of this board")
        row = state[r]
        return state[:r] + (row[:c] + self.to_move(state) + row[c + 1 :],) + state[r + 1 :]

    def winner(self, state: Board) -> str | None:
        """The player with ``k`` marks in a row, or ``None``."""
        for line in self.lines:
            r, c = line[0]
            mark = state[r][c]
            if mark != EMPTY and all(state[rr][cc] == mark for rr, cc in line):
                return mark
        return None

    def is_terminal(self, state: Board) -> bool:
        return self.winner(state) is not None or all(EMPTY not in row for row in state)

    def utility(self, state: Board, player: str) -> int:
        """+1 if ``player`` has won, −1 if they have lost, 0 otherwise (a draw)."""
        emit("utility", state=state)
        winner = self.winner(state)
        if winner is None:
            return 0
        return 1 if winner == player else -1


TIC_TAC_TOE = KInARow(3, 3, 3)
"""Classic tic-tac-toe: three in a row on a 3 × 3 board."""
