"""Alternative: the simplest evaluation, open lines, returned as a NumPy number.

Lines still open for `player` minus lines still open for the opponent, divided by
the number of lines plus one. It wins fewer games than the weighted version (7 wins,
5 draws, 0 losses) but passes; returning numpy.float64 is fine.
"""

import math

import numpy as np

from introai.games import Game

# ---------------------------------------------------------------------------------------
# Part A: answers.
# ---------------------------------------------------------------------------------------

EVAL_VALUES: list[int] | None = [-1, 3, 1]

DEPTH_ONE_MOVE: tuple[int, int] | None = (2, 0)


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def h_alpha_beta_search(game: Game, state, depth: int, evaluate) -> tuple[float, object]:
    """Alpha-beta that stops ``depth`` moves below ``state`` and evaluates there."""
    player = game.to_move(state)

    def max_value(s, alpha, beta, d):
        if game.is_terminal(s):
            return game.utility(s, player), None
        if d == 0:
            return evaluate(game, s, player), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a), alpha, beta, d - 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(s, alpha, beta, d):
        if game.is_terminal(s):
            return game.utility(s, player), None
        if d == 0:
            return evaluate(game, s, player), None
        v, move = math.inf, None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a), alpha, beta, d - 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -math.inf, math.inf, depth)


def evaluate(game, state, player: str) -> float:
    """Open lines for `player` minus open lines for the opponent, scaled into (-1, 1)."""
    opponent = "O" if player == "X" else "X"
    difference = 0
    for line in game.lines:
        marks = {state[r][c] for r, c in line}
        difference += (opponent not in marks) - (player not in marks)
    return np.float64(difference / (len(game.lines) + 1))
