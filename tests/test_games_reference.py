import math

import pytest

from introai.games import examples
from introai.games.examples import TIC_TAC_TOE_POSITIONS, tree_evaluation
from introai.games.kinarow import TIC_TAC_TOE, KInARow
from introai.games.reference import (
    alpha_beta_search,
    h_alpha_beta_search,
    minimax_search,
    minimax_value,
    open_lines,
    weighted_lines,
    zero_evaluation,
)
from introai.testing.games import evaluated_leaves, optimal_moves, positions_visited
from introai.trace import record

INF = math.inf


class CountingGame(KInARow):
    """Tic-tac-toe that counts result calls without storing events."""

    def __init__(self):
        super().__init__(3, 3, 3)
        self.calls = 0

    def result(self, state, action):
        self.calls += 1
        return super().result(state, action)


def strict_alpha_beta(game, state):
    """Alpha-beta with the strict cutoff rule (v > beta, v < alpha)."""
    player = game.to_move(state)

    def value(s, alpha, beta, maximizing):
        if game.is_terminal(s):
            return game.utility(s, player)
        v = -INF if maximizing else INF
        for a in game.actions(s):
            w = value(game.result(s, a), alpha, beta, not maximizing)
            if maximizing:
                v = max(v, w)
                if v > beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = min(v, w)
                if v < alpha:
                    return v
                beta = min(beta, v)
        return v

    return value(state, -INF, INF, True)


def pruned(tree, search=alpha_beta_search):
    with record(kinds={"utility"}) as trace:
        search(tree, tree.initial)
    seen = evaluated_leaves(trace)
    return [leaf for leaf in tree.leaves if leaf not in seen]


# --- minimax ---------------------------------------------------------------------------


def test_minimax_values_of_the_worked_tree():
    tree = examples.worked_tree()
    values = {node: minimax_value(tree, node, "MAX") for node in "ABCD"}
    assert values == {"A": 4, "B": 4, "C": 1, "D": 3}
    assert minimax_search(tree, "A") == (4, "B")


def test_minimax_values_of_the_exercise_tree():
    tree = examples.minimax_exercise()
    values = {node: minimax_value(tree, node, "MAX") for node in "ABCDEFG"}
    assert values == {"D": 7, "E": 5, "B": 5, "F": 6, "G": 9, "C": 6, "A": 6}
    assert minimax_search(tree, "A") == (6, "C")


def test_minimax_value_is_for_the_player_to_move():
    tree = examples.worked_tree()
    assert minimax_search(tree, "B") == (-4, "B1")
    assert minimax_search(tree, "B1") == (4, None)


def test_minimax_keeps_the_first_of_equal_moves():
    assert minimax_search(examples.ties_tree(), "A") == (3, "B")


def test_full_tic_tac_toe_tree():
    game = CountingGame()
    assert minimax_search(game, game.initial) == (0, (0, 0))
    assert game.calls == 549_945


@pytest.mark.parametrize(
    "key, value, moves",
    [
        ("win_now", 1, [(0, 1), (1, 2)]),
        ("block", 0, [(0, 1)]),
        ("fork", 1, None),
        ("o_to_move", 1, None),
        ("draw", 0, None),
    ],
)
def test_test_positions(key, value, moves):
    state = TIC_TAC_TOE_POSITIONS[key]
    found, move = minimax_search(TIC_TAC_TOE, state)
    assert found == value
    best = optimal_moves(TIC_TAC_TOE, state)
    assert move in best
    if moves is not None:
        assert best == moves


def test_test_positions_have_the_pinned_rows_and_players():
    assert TIC_TAC_TOE_POSITIONS == {
        "win_now": ("X.X", "OO.", "..."),
        "block": ("X..", ".OX", ".O."),
        "fork": ("XO.", ".X.", "..O"),
        "o_to_move": (".X.", ".O.", ".X."),
        "draw": ("X..", ".O.", "..."),
    }
    assert TIC_TAC_TOE.to_move(TIC_TAC_TOE_POSITIONS["o_to_move"]) == "O"
    assert all(
        TIC_TAC_TOE.to_move(TIC_TAC_TOE_POSITIONS[key]) == "X"
        for key in ("win_now", "block", "fork", "draw")
    )


def test_fork_has_no_immediate_win():
    state = TIC_TAC_TOE_POSITIONS["fork"]
    for action in TIC_TAC_TOE.actions(state):
        assert TIC_TAC_TOE.winner(TIC_TAC_TOE.result(state, action)) is None


# --- alpha-beta ------------------------------------------------------------------------


def test_alpha_beta_on_the_worked_tree():
    tree = examples.worked_tree()
    assert alpha_beta_search(tree, "A") == (4, "B")
    assert pruned(tree) == ["C2", "C3", "D3"]
    assert pruned(tree, strict_alpha_beta) == ["C2", "C3", "D3"]


def test_alpha_beta_on_the_exercise_trees():
    assert pruned(examples.minimax_exercise()) == ["O"]
    tree = examples.alpha_beta_exercise()
    assert alpha_beta_search(tree, "A") == (6, "B")
    assert minimax_search(tree, "A") == (6, "B")
    assert pruned(tree) == ["N", "U", "V"]
    assert pruned(tree, strict_alpha_beta) == ["N", "U", "V"]


def test_the_strict_rule_prunes_less_on_ties():
    tree = examples.ties_tree()
    assert pruned(tree) == ["C2"]
    assert pruned(tree, strict_alpha_beta) == []


@pytest.mark.parametrize("seed", range(5))
def test_alpha_beta_equals_minimax_on_random_trees(seed):
    tree = examples.random_game_tree(3, 4, seed)
    assert alpha_beta_search(tree, tree.initial) == minimax_search(tree, tree.initial)
    assert pruned(tree) == pruned(tree, strict_alpha_beta)
    assert pruned(tree)


def test_alpha_beta_on_tic_tac_toe():
    game = CountingGame()
    assert alpha_beta_search(game, game.initial) == (0, (0, 0))
    assert game.calls == 18_296
    game.calls = 0
    assert strict_alpha_beta(game, game.initial) == 0
    assert game.calls == 146_119


@pytest.mark.parametrize("key", list(TIC_TAC_TOE_POSITIONS))
def test_alpha_beta_on_the_test_positions(key):
    state = TIC_TAC_TOE_POSITIONS[key]
    value, move = alpha_beta_search(TIC_TAC_TOE, state)
    assert value == minimax_search(TIC_TAC_TOE, state)[0]
    assert move in optimal_moves(TIC_TAC_TOE, state)


def test_alpha_beta_reports_its_steps():
    tree = examples.worked_tree()
    with record(kinds={"alpha-beta"}) as trace:
        alpha_beta_search(tree, "A")
    rows = [
        (d["node"], d["outcome"], d["alpha"], d["beta"], d["value"], d["skipped"])
        for d in (event.data for event in trace.events)
    ]
    assert rows == [
        ("B1", "leaf", -INF, INF, 4, []),
        ("B2", "leaf", -INF, 4, 9, []),
        ("B3", "leaf", -INF, 4, 6, []),
        ("B", "return", -INF, 4, 4, []),
        ("C1", "leaf", 4, INF, 2, []),
        ("C", "cutoff", 4, 2, 2, ["C2", "C3"]),
        ("D1", "leaf", 4, INF, 5, []),
        ("D2", "leaf", 4, 5, 3, []),
        ("D", "cutoff", 4, 3, 3, ["D3"]),
        ("A", "return", 4, INF, 4, []),
    ]
    windows = {event.data["node"]: event.data["window"] for event in trace.events}
    assert windows["C"] == (4, INF)
    assert windows["D2"] == (4, 5)


def test_terminal_state_has_no_move():
    state = TIC_TAC_TOE.from_rows(["XXX", "OO.", "..."])
    assert minimax_search(TIC_TAC_TOE, state) == (-1, None)  # O is to move and has lost
    assert alpha_beta_search(TIC_TAC_TOE, state) == (-1, None)
    assert h_alpha_beta_search(TIC_TAC_TOE, state, 0, zero_evaluation) == (-1, None)


# --- depth-limited alpha-beta ----------------------------------------------------------


def test_cutoff_tree_gives_a_different_answer_at_each_depth():
    tree = examples.cutoff_tree()
    found = [h_alpha_beta_search(tree, "A", depth, tree_evaluation) for depth in (0, 1, 2, 3)]
    assert found == [(4, None), (6, "B"), (4, "C"), (5, "B")]
    assert h_alpha_beta_search(tree, "A", 3, tree_evaluation) == minimax_search(tree, "A")


def test_evaluation_tree_misleads_a_shallow_search():
    tree = examples.evaluation_tree()
    assert h_alpha_beta_search(tree, "A", 1, tree_evaluation) == (6, "D")
    assert h_alpha_beta_search(tree, "A", 2, tree_evaluation) == (4, "B")


def test_depth_limited_search_evaluates_only_at_the_cutoff():
    tree = examples.cutoff_tree()
    calls = []

    def evaluate(game, state, player):
        calls.append((state, player))
        return tree_evaluation(game, state, player)

    with record(kinds={"utility"}) as trace:
        h_alpha_beta_search(tree, "A", 1, evaluate)
    assert calls == [("B", "MAX"), ("C", "MAX")]
    assert trace.events == []


@pytest.mark.parametrize("key", list(TIC_TAC_TOE_POSITIONS))
def test_depth_limited_search_with_full_depth_equals_minimax(key):
    state = TIC_TAC_TOE_POSITIONS[key]
    value, move = h_alpha_beta_search(TIC_TAC_TOE, state, 9, zero_evaluation)
    assert value == minimax_search(TIC_TAC_TOE, state)[0]
    assert move in optimal_moves(TIC_TAC_TOE, state)


# --- evaluation functions --------------------------------------------------------------


def test_open_lines():
    state = ("X..", ".O.", "...")
    assert open_lines(TIC_TAC_TOE, TIC_TAC_TOE.initial, "X") == 0
    assert open_lines(TIC_TAC_TOE, state, "X") == pytest.approx(-1 / 9)
    assert open_lines(TIC_TAC_TOE, state, "O") == pytest.approx(1 / 9)


def test_weighted_lines():
    state = ("X..", ".O.", "...")
    assert weighted_lines(TIC_TAC_TOE, TIC_TAC_TOE.initial, "X") == 0
    assert weighted_lines(TIC_TAC_TOE, state, "X") == pytest.approx(-0.5)
    assert weighted_lines(TIC_TAC_TOE, state, "O") == pytest.approx(0.5)
    two = ("XX.", ".O.", "...")  # X has a line with two marks
    assert weighted_lines(TIC_TAC_TOE, two, "X") > weighted_lines(TIC_TAC_TOE, state, "X")


def test_evaluations_stay_strictly_between_loss_and_win():
    game = KInARow(5, 5, 4)
    state = game.from_rows(["XXX..", "XX...", "X....", "OOO..", "OOO.."])
    for evaluate in (open_lines, weighted_lines):
        for player in game.players:
            assert -1 < evaluate(game, state, player) < 1
    assert zero_evaluation(game, state, "X") == 0


# --- testing helpers -------------------------------------------------------------------


def test_positions_visited_counts_the_start_and_every_result():
    with record(kinds={"result"}) as trace:
        TIC_TAC_TOE.result(TIC_TAC_TOE.result(TIC_TAC_TOE.initial, (0, 0)), (1, 1))
    assert positions_visited(trace) == 3


def test_optimal_moves_on_a_tree():
    assert optimal_moves(examples.ties_tree(), "A") == ["B", "C"]
    assert optimal_moves(examples.worked_tree(), "B") == ["B1"]
