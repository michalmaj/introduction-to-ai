import pytest

from introai.games.examples import TIC_TAC_TOE_POSITIONS
from introai.games.kinarow import TIC_TAC_TOE, KInARow
from introai.games.players import (
    MATCH_OPENINGS,
    PlayResult,
    alpha_beta_player,
    match,
    play,
    random_player,
    search_player,
)
from introai.games.reference import (
    alpha_beta_search,
    open_lines,
    weighted_lines,
    zero_evaluation,
)


def test_random_player_is_reproducible_and_legal():
    first = play(TIC_TAC_TOE, {"X": random_player(1), "O": random_player(2)})
    again = play(TIC_TAC_TOE, {"X": random_player(1), "O": random_player(2)})
    assert first == again
    other = play(TIC_TAC_TOE, {"X": random_player(3), "O": random_player(4)})
    assert other.moves != first.moves
    assert len(set(first.moves)) == len(first.moves)


def test_two_perfect_players_draw():
    perfect = search_player(alpha_beta_search)
    result = play(TIC_TAC_TOE, {"X": perfect, "O": perfect})
    assert isinstance(result, PlayResult)
    assert result.winner is None
    assert len(result.moves) == 9
    assert TIC_TAC_TOE.is_terminal(result.state)


def test_play_from_a_given_state():
    perfect = search_player(alpha_beta_search)
    result = play(TIC_TAC_TOE, {"X": perfect, "O": perfect}, TIC_TAC_TOE_POSITIONS["win_now"])
    assert result == PlayResult("X", ("XXX", "OO.", "..."), [(0, 1)])


def test_play_rejects_an_illegal_move():
    lazy = {"X": lambda game, state: None, "O": random_player(0)}
    with pytest.raises(ValueError, match="X"):
        play(TIC_TAC_TOE, lazy)


def test_match_openings_are_pinned():
    assert MATCH_OPENINGS == [
        [(2, 2), (1, 1)],
        [(2, 2), (0, 0)],
        [(0, 0), (2, 2)],
        [(1, 2), (2, 2)],
        [(2, 1), (2, 3)],
        [(0, 4), (4, 0)],
    ]


def flipped(game, state, player):
    return -weighted_lines(game, state, player)


@pytest.mark.parametrize(
    "evaluate, wins, draws, losses",
    [
        (weighted_lines, 11, 1, 0),
        (open_lines, 7, 5, 0),
        (zero_evaluation, 3, 6, 3),
        (flipped, 1, 9, 2),
    ],
    ids=["weighted", "open_lines", "zero", "flipped"],
)
def test_match_against_a_player_without_an_evaluation(evaluate, wins, draws, losses):
    game = KInARow(5, 5, 4)
    table = match(game, alpha_beta_player(2, evaluate), alpha_beta_player(2, zero_evaluation))
    assert (table["win"], table["draw"], table["loss"]) == (wins, draws, losses)
