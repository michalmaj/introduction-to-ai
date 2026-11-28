"""Alternative: negamax, one function for both players.

In a zero-sum game a position worth v to one player is worth −v to the other, so
"the value for the player to move" is the largest of the negated values of the
children.
"""

from introai.games import Game

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise tree.
# ---------------------------------------------------------------------------------------

MINIMAX_VALUES: dict[str, int | None] = {
    "A": 6,
    "B": 5,
    "C": 6,
    "D": 7,
    "E": 5,
    "F": 6,
    "G": 9,
}

BEST_MOVE: str | None = "C"


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def minimax_search(game: Game, state) -> tuple[float, object]:
    """Negamax: value(s) = max over moves of −value(child), for the player to move."""
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)), None
    v, move = -float("inf"), None
    for a in game.actions(state):
        v2 = -minimax_search(game, game.result(state, a))[0]
        if v2 > v:
            v, move = v2, a
    return v, move
