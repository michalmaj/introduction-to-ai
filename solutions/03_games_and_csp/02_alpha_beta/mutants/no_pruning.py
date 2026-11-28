"""Mutant: keeps α and β up to date but never cuts off.

Violated requirement: a node stops searching as soon as v >= β (MAX) or v <= α (MIN).
Common mistake in the lesson: "Bounds without a cutoff".
"""

import math

from introai.games import Game

CAUGHT_BY = (
    "test_alpha_beta_visits_far_fewer_positions_than_minimax",
    "test_alpha_beta_prunes_like_the_lesson",
)

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise tree.
# ---------------------------------------------------------------------------------------

PRUNED_LEAVES: set[str] | None = {"N", "U", "V"}


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def alpha_beta_search(game: Game, state) -> tuple[float, object]:
    """Alpha-beta that computes the bounds and never uses them."""
    player = game.to_move(state)

    def max_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if False:
                return v, move
        return v, move

    def min_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = math.inf, None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if False:
                return v, move
        return v, move

    return max_value(state, -math.inf, math.inf)
