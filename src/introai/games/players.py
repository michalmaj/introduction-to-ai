"""Players and matches.

A player is a function ``player(game, state) -> move``. Matches start from fixed
openings and swap colours, so every result is reproducible.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field

from introai.games.core import Action, Game, State
from introai.games.reference import h_alpha_beta_search

Strategy = Callable[[Game, State], Action]
"""A player: a function that picks a move in a state."""


def random_player(seed: int) -> Strategy:
    """A player that picks a legal move at random; the same seed gives the same moves."""
    rng = random.Random(seed)
    return lambda game, state: rng.choice(list(game.actions(state)))


def search_player(search, **kwargs) -> Strategy:
    """A player that plays the move ``search(game, state, **kwargs)`` returns."""
    return lambda game, state: search(game, state, **kwargs)[1]


def alpha_beta_player(depth: int, evaluate) -> Strategy:
    """A player that uses the reference depth-limited alpha-beta with ``evaluate``."""
    return search_player(h_alpha_beta_search, depth=depth, evaluate=evaluate)


@dataclass(frozen=True)
class PlayResult:
    """How a game ended: the winner (``None`` for a draw), the final state, the moves played."""

    winner: str | None
    state: State
    moves: list[Action] = field(default_factory=list)


def play(game: Game, players: Mapping[str, Strategy], state: State | None = None) -> PlayResult:
    """Play from ``state`` (the initial state by default) until the game ends."""
    state = game.initial if state is None else state
    moves = []
    while not game.is_terminal(state):
        mover = game.to_move(state)
        move = players[mover](game, state)
        if move not in game.actions(state):
            raise ValueError(f"player {mover} chose {move!r}, which is not a legal move here")
        moves.append(move)
        state = game.result(state, move)
    winner = next((p for p in game.players if game.utility(state, p) > 0), None)
    return PlayResult(winner, state, moves)


MATCH_OPENINGS: list[list[tuple[int, int]]] = [
    [(2, 2), (1, 1)],
    [(2, 2), (0, 0)],
    [(0, 0), (2, 2)],
    [(1, 2), (2, 2)],
    [(2, 1), (2, 3)],
    [(0, 4), (4, 0)],
]
"""The first two moves of every match game on the 5 × 5 board (lesson 3.3)."""


def match(
    game: Game,
    tested: Strategy,
    opponent: Strategy,
    openings: Sequence[Sequence[Action]] = MATCH_OPENINGS,
) -> Counter:
    """Play every opening twice, ``tested`` once with each colour; count its results.

    The counter has the keys ``"win"``, ``"draw"`` and ``"loss"``.
    """
    table = Counter({"win": 0, "draw": 0, "loss": 0})
    for opening in openings:
        start = game.initial
        for move in opening:
            start = game.result(start, move)
        for side in game.players:
            other = next(p for p in game.players if p != side)
            result = play(game, {side: tested, other: opponent}, start)
            if result.winner is None:
                table["draw"] += 1
            else:
                table["win" if result.winner == side else "loss"] += 1
    return table
