"""Mutant: at the depth limit it evaluates even a state where the game is over.

Violated requirement: a terminal state always gets its utility.
Common mistake in the lesson: "A win that is only estimated".
"""

import math

from introai.games import Game

CAUGHT_BY = ("test_h_search_takes_an_immediate_win",)

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
        if d == 0:
            return evaluate(game, s, player), None
        if game.is_terminal(s):
            return game.utility(s, player), None
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
        if d == 0:
            return evaluate(game, s, player), None
        if game.is_terminal(s):
            return game.utility(s, player), None
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
    """Lines with marks of only one player, worth 10**(marks - 1); squeezed into (-1, 1)."""
    opponent = "O" if player == "X" else "X"
    score = 0
    for line in game.lines:
        marks = [state[r][c] for r, c in line]
        mine, theirs = marks.count(player), marks.count(opponent)
        if mine and not theirs:
            score += 10 ** (mine - 1)
        elif theirs and not mine:
            score -= 10 ** (theirs - 1)
    return score / (1 + abs(score))
