"""Helpers for testing game-playing searches through their trace."""

from __future__ import annotations

from introai.games.core import Game, State
from introai.games.reference import minimax_value
from introai.trace import Trace


def evaluated_leaves(trace: Trace) -> list[State]:
    """The states passed to ``utility``, in order: the leaves a search looked at."""
    return [event.data["state"] for event in trace.of_kind("utility")]


def positions_visited(trace: Trace) -> int:
    """The positions one search visited: its start plus every state made by ``result``."""
    return 1 + len(trace.of_kind("result"))


def optimal_moves(game: Game, state: State) -> list:
    """Every move with the best minimax value for the player to move, in ``actions`` order."""
    player = game.to_move(state)
    values = {a: minimax_value(game, game.result(state, a), player) for a in game.actions(state)}
    best = max(values.values(), default=None)
    return [a for a, value in values.items() if value == best]
