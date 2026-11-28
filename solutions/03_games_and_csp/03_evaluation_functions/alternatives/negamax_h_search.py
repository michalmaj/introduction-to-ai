"""Alternative: negamax with alpha-beta and a depth limit.

One function for both players. At the cutoff it evaluates for the player to move
there; the parent negates the value, which is the same as evaluating for the other
player when the evaluation is symmetric (good for X is equally bad for O).
"""

import math

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
    """Negamax alpha-beta that stops ``depth`` moves below ``state``."""

    def value(s, alpha, beta, d):
        if game.is_terminal(s):
            return game.utility(s, game.to_move(s)), None
        if d == 0:
            return evaluate(game, s, game.to_move(s)), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2 = -value(game.result(s, a), -beta, -alpha, d - 1)[0]
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    return value(state, -math.inf, math.inf, depth)


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
