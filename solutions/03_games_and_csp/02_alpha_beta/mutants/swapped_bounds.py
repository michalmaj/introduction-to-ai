"""Mutant: passes α and β to the children in the wrong order.

Violated requirement: a child gets (α, β), the guarantees of MAX and MIN.
Common mistake in the lesson: "Swapped bounds".
"""

import math

from introai.games import Game

CAUGHT_BY = ("test_alpha_beta_value_equals_minimax_on_trees",)

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise tree.
# ---------------------------------------------------------------------------------------

PRUNED_LEAVES: set[str] | None = {"N", "U", "V"}


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def alpha_beta_search(game: Game, state) -> tuple[float, object]:
    """Alpha-beta that swaps α and β on the way down."""
    player = game.to_move(state)

    def max_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a), beta, alpha)
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
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a), beta, alpha)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -math.inf, math.inf)
