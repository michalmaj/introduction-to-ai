"""Lesson 3.2: alpha-beta pruning.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: prune the exercise tree by hand and write down the leaves alpha-beta never looks at.
Part B: implement alpha_beta_search().

Check your work from the repository root:

    uv run pytest modules/03_games_and_csp/02_alpha_beta
"""

from introai.games import Game

# ---------------------------------------------------------------------------------------
# Part A: prune it by hand.
# The tree and the exact rules are in the lesson, section "Your turn".
# ---------------------------------------------------------------------------------------

# The leaves alpha-beta never looks at, as a set of names, for example {"K", "L"}.
PRUNED_LEAVES: set[str] | None = None


# ---------------------------------------------------------------------------------------
# Part B: implementation.
#   - the same contract as minimax_search in lesson 3.1: return (value, move), the value
#     for the player to move at `state`, the move None when the game is over;
#   - search the moves in the order of game.actions;
#   - cut off as soon as v >= beta in a MAX node or v <= alpha in a MIN node.
# ---------------------------------------------------------------------------------------


def alpha_beta_search(game: Game, state) -> tuple[float, object]:
    """Minimax with alpha-beta pruning: the same value and move, much less work."""
    raise NotImplementedError(
        "TODO: implement alpha_beta_search in task.py (or set IMPLEMENTATION = "
        '"reference" in the notebook\'s first cell)'
    )
