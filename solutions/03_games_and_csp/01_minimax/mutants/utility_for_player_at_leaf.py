"""Mutant: a leaf is scored for the player to move at the leaf, not at the root.

Violated requirement: every value is for the player to move at `state`.
Common mistake in the lesson: "Whose utility?".
"""

from introai.games import Game

CAUGHT_BY = ("test_minimax_values_on_trees",)

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
    """Minimax that asks game.utility(leaf, game.to_move(leaf))."""

    def max_value(s):
        if game.is_terminal(s):
            return game.utility(s, game.to_move(s)), None
        v, move = -float("inf"), None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(s):
        if game.is_terminal(s):
            return game.utility(s, game.to_move(s)), None
        v, move = float("inf"), None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)
