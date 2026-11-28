"""Lesson 3.1: reference solution."""

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
    """The best move for the player to move in ``state``, with its minimax value."""
    player = game.to_move(state)

    def max_value(s):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = -float("inf"), None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(s):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = float("inf"), None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)
