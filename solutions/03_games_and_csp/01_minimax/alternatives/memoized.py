"""Alternative: minimax that remembers the value of every position it has solved.

Tic-tac-toe has 549,946 nodes in its game tree but only 5,478 distinct positions:
the same position is reached by many move orders. A dictionary of solved positions
(like the reached set of lesson 2.1) turns the tree back into a graph.
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
    """Minimax with a dictionary of positions already solved during this call."""
    player = game.to_move(state)
    solved: dict = {}

    def value(s):
        if s not in solved:
            if game.is_terminal(s):
                solved[s] = game.utility(s, player), None
            else:
                pick = max if game.to_move(s) == player else min
                options = [(value(game.result(s, a))[0], a) for a in game.actions(s)]
                best = pick(v for v, _ in options)
                solved[s] = best, next(a for v, a in options if v == best)
        return solved[s]

    return value(state)
