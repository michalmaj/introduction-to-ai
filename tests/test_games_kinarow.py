import pytest

from introai.games.kinarow import TIC_TAC_TOE, KInARow
from introai.trace import record


def test_initial_state_is_a_tuple_of_empty_rows():
    assert TIC_TAC_TOE.initial == ("...", "...", "...")
    assert KInARow(2, 4, 3).initial == ("....", "....")
    assert TIC_TAC_TOE.players == ("X", "O")


@pytest.mark.parametrize("m, n, k", [(0, 3, 3), (3, 3, 0), (3, 3, 4), (2, 2, 3)])
def test_impossible_boards_are_rejected(m, n, k):
    with pytest.raises(ValueError):
        KInARow(m, n, k)


def test_from_rows_returns_the_state():
    assert TIC_TAC_TOE.from_rows(["X..", ".O.", "..."]) == ("X..", ".O.", "...")


@pytest.mark.parametrize(
    "rows",
    [
        ["X..", ".O."],
        ["X...", ".O.", "..."],
        ["X..", ".o.", "..."],
        ["XX.", "...", "..."],
        ["O..", "...", "..."],
        "X..\n.O.\n...",
    ],
    ids=["too_few_rows", "long_row", "unknown_mark", "x_too_many", "o_first", "one_string"],
)
def test_from_rows_rejects_invalid_boards(rows):
    with pytest.raises(ValueError):
        TIC_TAC_TOE.from_rows(rows)


def test_to_move_follows_the_counts_of_marks():
    assert TIC_TAC_TOE.to_move(TIC_TAC_TOE.initial) == "X"
    assert TIC_TAC_TOE.to_move(("X..", "...", "...")) == "O"
    assert TIC_TAC_TOE.to_move(("X..", ".O.", "...")) == "X"


def test_actions_are_the_empty_cells_in_row_major_order():
    state = TIC_TAC_TOE.from_rows(["X.O", "...", "OXX"])
    assert TIC_TAC_TOE.actions(state) == [(0, 1), (1, 0), (1, 1), (1, 2)]


def test_result_places_the_mark_of_the_player_to_move():
    state = TIC_TAC_TOE.result(TIC_TAC_TOE.initial, (1, 1))
    assert state == ("...", ".X.", "...")
    assert TIC_TAC_TOE.result(state, (0, 2)) == ("..O", ".X.", "...")


@pytest.mark.parametrize("action", [(0, 0), (3, 0), (-1, 0), (0, 3), None, "a1"])
def test_result_rejects_occupied_and_missing_cells(action):
    with pytest.raises(ValueError):
        TIC_TAC_TOE.result(("X..", "...", "..."), action)


@pytest.mark.parametrize(
    "rows, winner",
    [
        (["XXX", "OO.", "..."], "X"),
        (["XO.", "XO.", "X.."], "X"),
        (["OX.", "XO.", "X.O"], "O"),
        (["X.O", "XO.", "O.X"], "O"),
    ],
    ids=["row", "column", "diagonal", "anti_diagonal"],
)
def test_a_line_wins_and_ends_the_game(rows, winner):
    state = TIC_TAC_TOE.from_rows(rows)
    loser = "O" if winner == "X" else "X"
    assert TIC_TAC_TOE.winner(state) == winner
    assert TIC_TAC_TOE.is_terminal(state)
    assert TIC_TAC_TOE.utility(state, winner) == 1
    assert TIC_TAC_TOE.utility(state, loser) == -1


def test_a_full_board_without_a_line_is_a_draw():
    state = TIC_TAC_TOE.from_rows(["XOX", "XOO", "OXX"])
    assert TIC_TAC_TOE.winner(state) is None
    assert TIC_TAC_TOE.is_terminal(state)
    assert TIC_TAC_TOE.utility(state, "X") == 0
    assert TIC_TAC_TOE.utility(state, "O") == 0


def test_a_game_in_progress_is_not_terminal():
    assert not TIC_TAC_TOE.is_terminal(("X..", ".O.", "..."))
    assert TIC_TAC_TOE.winner(("X..", ".O.", "...")) is None


def test_lines_of_the_boards():
    assert len(TIC_TAC_TOE.lines) == 8
    assert ((0, 0), (1, 1), (2, 2)) in TIC_TAC_TOE.lines
    assert ((0, 2), (1, 1), (2, 0)) in TIC_TAC_TOE.lines
    assert len(KInARow(5, 5, 4).lines) == 28


def test_four_in_a_row_on_a_five_by_five_board():
    game = KInARow(5, 5, 4)
    three = game.from_rows(["X....", ".X...", "..X..", "OO...", "O...."])
    assert game.winner(three) is None
    four = game.result(three, (3, 3))
    assert game.winner(four) == "X"
    assert game.is_terminal(four)


def test_render_shows_one_row_per_line():
    assert TIC_TAC_TOE.render(("X..", ".O.", "...")) == "X..\n.O.\n..."


def test_result_and_utility_report_events_under_record():
    TIC_TAC_TOE.result(TIC_TAC_TOE.initial, (2, 2))  # nobody listens: nothing is stored
    with record() as trace:
        state = TIC_TAC_TOE.result(TIC_TAC_TOE.initial, (0, 0))
        TIC_TAC_TOE.utility(state, "X")
    assert [event.kind for event in trace.events] == ["result", "utility"]
    assert trace.events[0].data == {"state": TIC_TAC_TOE.initial, "action": (0, 0)}
    assert trace.events[1].data == {"state": state}
