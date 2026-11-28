"""Lesson 3.1: games and minimax.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: compute the minimax values of the exercise tree by hand and write them below.
Part B: implement minimax_search().

Check your work from the repository root:

    uv run pytest modules/03_games_and_csp/01_minimax
"""

from introai.games import Game

# ---------------------------------------------------------------------------------------
# Part A: compute it by hand.
# The tree is in the lesson, section "Your turn". Values are from MAX's point of view.
# ---------------------------------------------------------------------------------------

# The minimax value of every inner node of the exercise tree.
MINIMAX_VALUES: dict[str, int | None] = {
    "A": None,
    "B": None,
    "C": None,
    "D": None,
    "E": None,
    "F": None,
    "G": None,
}

# The move MAX should make at the root A: "B" or "C".
BEST_MOVE: str | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - use only game.to_move, game.actions, game.result, game.is_terminal and game.utility;
#   - return (value, move): the value of `state` for the player to move there, and the move
#     that achieves it; when the game is already over, the move is None;
#   - the same function must work for tic-tac-toe and for the small trees of the lesson.
# ---------------------------------------------------------------------------------------


def minimax_search(game: Game, state) -> tuple[float, object]:
    """The best move for the player to move in ``state``, with its minimax value."""
    raise NotImplementedError(
        "TODO: implement minimax_search in task.py (or set IMPLEMENTATION = "
        '"reference" in the notebook\'s first cell)'
    )
