"""Alternative: negamax with alpha-beta, one function for both players.

The value for the player to move is the largest of the negated values of the
children; the window (α, β) of one player is (−β, −α) for the other.
"""

import math

from introai.games import Game

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise tree.
# ---------------------------------------------------------------------------------------

PRUNED_LEAVES: set[str] | None = {"N", "U", "V"}


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def alpha_beta_search(game: Game, state) -> tuple[float, object]:
    """Negamax alpha-beta: one function, the window flips sign at every level."""

    def value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, game.to_move(s)), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2 = -value(game.result(s, a), -beta, -alpha)[0]
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    return value(state, -math.inf, math.inf)
