"""Lesson 3.3: evaluation functions and depth limits.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: evaluate three positions by hand and find the move a depth-1 search makes.
Part B: implement h_alpha_beta_search() and your own evaluate().

Check your work from the repository root:

    uv run pytest modules/03_games_and_csp/03_evaluation_functions
"""

from introai.games import Game

# ---------------------------------------------------------------------------------------
# Part A: compute it by hand.
# The positions and the evaluation e are in the lesson, section "Your turn".
# ---------------------------------------------------------------------------------------

# e for the three positions of "Your turn", in order, for example [0, 0, 0].
EVAL_VALUES: list[int] | None = None

# The move (row, col) X chooses in the position of "Your turn" with a depth-1 search and e.
DEPTH_ONE_MOVE: tuple[int, int] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - h_alpha_beta_search is alpha-beta from lesson 3.2 with a depth limit: a terminal state
#     gets its utility; a state `depth` moves below `state` that is not terminal gets
#     evaluate(game, s, player), with `player` the player to move at `state`;
#   - evaluate(game, state, player) works for any k-in-a-row board: game.lines lists every
#     winning line as cells (row, col), and state[row][col] is "X", "O" or ".";
#     it returns a number between -1 (as bad as a loss) and 1 (as good as a win).
# ---------------------------------------------------------------------------------------


def h_alpha_beta_search(game: Game, state, depth: int, evaluate) -> tuple[float, object]:
    """Alpha-beta that stops ``depth`` moves below ``state`` and evaluates there."""
    raise NotImplementedError(
        "TODO: implement h_alpha_beta_search in task.py (or set IMPLEMENTATION = "
        '"reference" in the notebook\'s first cell)'
    )


def evaluate(game, state, player: str) -> float:
    """How good a position that is not over is for ``player``, between -1 and 1."""
    raise NotImplementedError(
        "TODO: implement evaluate in task.py (or set IMPLEMENTATION = "
        '"reference" in the notebook\'s first cell)'
    )
