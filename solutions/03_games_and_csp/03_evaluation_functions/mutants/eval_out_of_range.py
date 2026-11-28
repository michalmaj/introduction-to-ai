"""Mutant: returns the raw weighted sum, which can be far above 1.

Violated requirement: an evaluation lies between -1 (a loss) and 1 (a win).
Common mistake in the lesson: "A promise bigger than a win".
"""

import math

from introai.games import Game

CAUGHT_BY = ("test_evaluation_stays_between_loss_and_win",)

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
    """Weighted lines without squeezing."""
    opponent = "O" if player == "X" else "X"
    score = 0
    for line in game.lines:
        marks = [state[r][c] for r, c in line]
        mine, theirs = marks.count(player), marks.count(opponent)
        if mine and not theirs:
            score += 10 ** (mine - 1)
        elif theirs and not mine:
            score -= 10 ** (theirs - 1)
    return score
