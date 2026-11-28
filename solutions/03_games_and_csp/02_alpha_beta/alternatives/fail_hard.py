"""Alternative: fail-hard alpha-beta, whose values never leave the window [α, β].

After a cutoff a MAX node returns β itself (and a MIN node α) instead of v, and a
node that cannot reach the window returns the bound. The value at the root, searched
with the window (−∞, +∞), is still exact.
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
    """Alpha-beta that clamps every returned value into [α, β]."""
    player = game.to_move(state)

    def max_value(s, alpha, beta):
        if game.is_terminal(s):
            return min(max(game.utility(s, player), alpha), beta), None
        move = None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a), alpha, beta)
            if v2 >= beta:
                return beta, a
            if v2 > alpha or move is None:
                if v2 > alpha:
                    alpha = v2
                move = a
        return alpha, move

    def min_value(s, alpha, beta):
        if game.is_terminal(s):
            return min(max(game.utility(s, player), alpha), beta), None
        move = None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a), alpha, beta)
            if v2 <= alpha:
                return alpha, a
            if v2 < beta or move is None:
                if v2 < beta:
                    beta = v2
                move = a
        return beta, move

    return max_value(state, -math.inf, math.inf)
