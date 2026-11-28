"""Reference game-playing searches and evaluation functions.

These are the course's own versions of what students write in lessons 3.1–3.3.
Every search returns ``(value, move)``: the value of ``state`` for the player to
move there, and the move that achieves it (``None`` when the game is over). Of
moves with equal value the first in ``actions`` order is kept.
"""

from __future__ import annotations

import math

from introai.games.core import Game, Player, State
from introai.trace import emit, wants


def minimax_value(game: Game, state: State, player: Player) -> float:
    """The minimax value of ``state`` for ``player``."""
    if game.is_terminal(state):
        return game.utility(state, player)
    values = [minimax_value(game, game.result(state, a), player) for a in game.actions(state)]
    return max(values) if game.to_move(state) == player else min(values)


def minimax_search(game: Game, state: State):
    """The move with the best minimax value for the player to move (lesson 3.1)."""
    player = game.to_move(state)

    def max_value(s):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(s):
        if game.is_terminal(s):
            return game.utility(s, player), None
        v, move = math.inf, None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)


def alpha_beta_search(game: Game, state: State):
    """Minimax with alpha-beta pruning, cutting off at ``v >= β`` and ``v <= α`` (lesson 3.2).

    With a recording that keeps ``"alpha-beta"`` events, every leaf and every
    finished inner node is reported with α, β and v at that moment, the window
    (α, β) it was entered with, and the moves it skipped after a cutoff.
    """
    player = game.to_move(state)

    def report(s, outcome, alpha, beta, v, window, skipped=()):
        if wants("alpha-beta"):
            emit(
                "alpha-beta",
                node=s,
                outcome=outcome,
                alpha=alpha,
                beta=beta,
                value=v,
                window=window,
                skipped=list(skipped),
            )

    def max_value(s, alpha, beta):
        if game.is_terminal(s):
            v = game.utility(s, player)
            report(s, "leaf", alpha, beta, v, (alpha, beta))
            return v, None
        window = (alpha, beta)
        v, move = -math.inf, None
        actions = game.actions(s)
        for i, a in enumerate(actions):
            v2, _ = min_value(game.result(s, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                report(s, "cutoff", alpha, beta, v, window, actions[i + 1 :])
                return v, move
        report(s, "return", alpha, beta, v, window)
        return v, move

    def min_value(s, alpha, beta):
        if game.is_terminal(s):
            v = game.utility(s, player)
            report(s, "leaf", alpha, beta, v, (alpha, beta))
            return v, None
        window = (alpha, beta)
        v, move = math.inf, None
        actions = game.actions(s)
        for i, a in enumerate(actions):
            v2, _ = max_value(game.result(s, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                report(s, "cutoff", alpha, beta, v, window, actions[i + 1 :])
                return v, move
        report(s, "return", alpha, beta, v, window)
        return v, move

    return max_value(state, -math.inf, math.inf)


def h_alpha_beta_search(game: Game, state: State, depth: int, evaluate):
    """Alpha-beta that stops ``depth`` moves below ``state`` (lesson 3.3).

    A terminal state gets its utility; a state at the depth limit that is not
    terminal gets ``evaluate(game, state, player)``, with ``player`` the player to
    move at ``state``.
    """
    player = game.to_move(state)

    def max_value(s, alpha, beta, d):
        if game.is_terminal(s):
            return game.utility(s, player), None
        if d == 0:
            return evaluate(game, s, player), None
        v, move = -math.inf, None
        for a in game.actions(s):
            v2, _ = min_value(game.result(s, a), alpha, beta, d - 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(s, alpha, beta, d):
        if game.is_terminal(s):
            return game.utility(s, player), None
        if d == 0:
            return evaluate(game, s, player), None
        v, move = math.inf, None
        for a in game.actions(s):
            v2, _ = max_value(game.result(s, a), alpha, beta, d - 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -math.inf, math.inf, depth)


def _opponent(game: Game, player: Player) -> Player:
    first, second = game.players
    return second if player == first else first


def zero_evaluation(game: Game, state: State, player: Player) -> float:
    """An evaluation that knows nothing: every position is worth 0."""
    return 0.0


def open_lines(game, state, player: Player) -> float:
    """Lines still open for ``player`` minus lines still open for the opponent.

    A line is open for a player while the opponent has no mark on it. The
    difference is divided by the number of lines plus one, so the result lies
    strictly between −1 (a loss) and 1 (a win).
    """
    opponent = _opponent(game, player)
    difference = 0
    for line in game.lines:
        marks = {state[r][c] for r, c in line}
        difference += (opponent not in marks) - (player not in marks)
    return difference / (len(game.lines) + 1)


def weighted_lines(game, state, player: Player) -> float:
    """Lines with marks of only one player, worth 10**(marks − 1) each.

    Lines of ``player`` count plus, lines of the opponent minus; the sum *x* is
    squeezed into (−1, 1) as *x* / (1 + |*x*|).
    """
    opponent = _opponent(game, player)
    score = 0
    for line in game.lines:
        marks = [state[r][c] for r, c in line]
        mine, theirs = marks.count(player), marks.count(opponent)
        if mine and not theirs:
            score += 10 ** (mine - 1)
        elif theirs and not mine:
            score -= 10 ** (theirs - 1)
    return score / (1 + abs(score))
