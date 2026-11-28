"""Mutant: computes the right value but returns the first legal move.

Violated requirement: the move returned is one that achieves the value.
Common mistake in the lesson: "The value without the move".
"""

from introai.games import Game

CAUGHT_BY = ("test_returns_an_optimal_move",)

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
    """Correct values, but the move is simply the first one."""
    player = game.to_move(state)

    def value(s):
        if game.is_terminal(s):
            return game.utility(s, player)
        values = [value(game.result(s, a)) for a in game.actions(s)]
        return max(values) if game.to_move(s) == player else min(values)

    if game.is_terminal(state):
        return game.utility(state, player), None
    return value(state), game.actions(state)[0]
