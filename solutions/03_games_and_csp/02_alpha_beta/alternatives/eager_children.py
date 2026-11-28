"""Alternative: builds all the children of a node before searching them.

It prunes exactly the same leaves, but generates children it will never search, so
it calls game.result more often (25,226 times instead of 18,296 from the empty board).
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
    """Alpha-beta that generates every child up front."""
    player = game.to_move(state)

    def max_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = -math.inf, None
        children = [(a, game.result(s, a)) for a in game.actions(s)]
        for a, child in children:
            v2, _ = min_value(child, alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = math.inf, None
        children = [(a, game.result(s, a)) for a in game.actions(s)]
        for a, child in children:
            v2, _ = max_value(child, alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -math.inf, math.inf)
