"""Mutant: looks only one move ahead; a position that is not over is worth 0.

Violated requirement: minimax searches to the end of the game.
Common mistake in the lesson: "Looking one move ahead".
"""

from introai.games import Game

CAUGHT_BY = ("test_finds_a_forced_win",)

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
    """Pick the move whose resulting position is best right now."""
    player = game.to_move(state)
    if game.is_terminal(state):
        return game.utility(state, player), None
    v, move = -float("inf"), None
    for a in game.actions(state):
        child = game.result(state, a)
        v2 = game.utility(child, player) if game.is_terminal(child) else 0
        if v2 > v:
            v, move = v2, a
    return v, move
