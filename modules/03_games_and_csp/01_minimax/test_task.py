"""Self-check for lesson 3.1: games and minimax.

Run from the repository root:

    uv run pytest modules/03_games_and_csp/01_minimax

The tests check what every correct minimax does (the values, the perspective of
the player to move, optimal moves, forced wins, the end of the game), not one
way of writing it: a negamax version or one that remembers positions passes too.
"""

import pytest

from introai.games.examples import (
    TIC_TAC_TOE_POSITIONS,
    minimax_exercise,
    random_game_tree,
    ties_tree,
    worked_tree,
)
from introai.games.kinarow import TIC_TAC_TOE
from introai.games.reference import minimax_value
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.games import optimal_moves
from introai.trace import TraceLimitExceeded, record

LIMIT = 200_000  # calls of game.result during one search
STEP_BUDGET = 5_000_000  # lines executed in task.py during one search

TREES = {
    "worked_tree": worked_tree,
    "ties_tree": ties_tree,
    "random_tree": lambda: random_game_tree(3, 4, seed=0),
    "random_odd_tree": lambda: random_game_tree(2, 5, seed=1),
}
CONVENTION = (
    "the value is for the player to move at `state` (game.to_move(state)), and a leaf is "
    "scored with game.utility(leaf, that player)"
)


def search(impl, game, state):
    """Call impl.minimax_search(game, state); turn endless runs into hints."""
    failure = None
    try:
        with record(limit=LIMIT, kinds={"result"}), step_budget(impl.__file__, STEP_BUDGET):
            found = impl.minimax_search(game, state)
    except TraceLimitExceeded:
        failure = (
            f"minimax_search called game.result more than {LIMIT} times on a small "
            "position — does every branch stop at a terminal state?"
        )
    except RecursionError:
        failure = "minimax_search recursed too deeply — does it stop at terminal states?"
    except StepBudgetExceeded:
        failure = "minimax_search ran for too long — is there a loop that never ends?"
    if failure:
        pytest.fail(failure, pytrace=False)
    if not isinstance(found, tuple) or len(found) != 2:
        pytest.fail(
            f"minimax_search must return a pair (value, move), got {found!r}", pytrace=False
        )
    return found


# --- Part A: minimax by hand -----------------------------------------------------------


def test_part_a_minimax_values(impl):
    # pytrace=False: no traceback, so pytest cannot print `expected`. Never reveal it.
    tree = minimax_exercise()
    expected = {node: minimax_value(tree, node, "MAX") for node in tree.children}
    values = impl.MINIMAX_VALUES
    if not isinstance(values, dict):
        pytest.fail("Part A: MINIMAX_VALUES must be a dictionary", pytrace=False)
    missing = sorted(node for node in expected if values.get(node) is None)
    if missing:
        pytest.fail(f"Part A: fill in MINIMAX_VALUES for {', '.join(missing)}", pytrace=False)
    if not all(
        isinstance(values[node], int | float) and not isinstance(values[node], bool)
        for node in expected
    ):
        pytest.fail("Part A: every value in MINIMAX_VALUES must be a number", pytrace=False)
    wrong = sum(values[node] != expected[node] for node in expected)
    if wrong:
        pytest.fail(
            f"Part A: {wrong} of the {len(expected)} values in MINIMAX_VALUES are not right "
            "yet. Work up from the leaves: a MAX node takes the largest value of its "
            "children, a MIN node the smallest.",
            pytrace=False,
        )


def test_part_a_best_move(impl):
    tree = minimax_exercise()
    move = impl.BEST_MOVE
    if move is None:
        pytest.fail("Part A: fill in BEST_MOVE in task.py", pytrace=False)
    if move not in tree.actions("A"):
        pytest.fail(f"Part A: BEST_MOVE must be one of {tree.actions('A')}", pytrace=False)
    best = max(tree.actions("A"), key=lambda child: minimax_value(tree, child, "MAX"))
    if move != best:
        pytest.fail(
            "Part A: BEST_MOVE is not right yet — MAX moves to the child with the largest "
            "minimax value.",
            pytrace=False,
        )


# --- Part B: minimax_search ------------------------------------------------------------


@pytest.mark.parametrize("name", TREES)
def test_minimax_values_on_trees(impl, name):
    tree = TREES[name]()
    wrong = []
    for node in tree.children:
        value, _ = search(impl, tree, node)
        if value != minimax_value(tree, node, tree.to_move(node)):
            wrong.append((node, value))
    if wrong:
        node, value = wrong[0]
        pytest.fail(
            f"minimax_search returned a wrong value at {len(wrong)} of the "
            f"{len(tree.children)} inner nodes of {name}, for example {value!r} at {node!r} "
            f"(a {tree.to_move(node)} node). Remember: {CONVENTION}; MAX takes the largest "
            "value of the children, MIN the smallest.",
            pytrace=False,
        )


def test_value_is_for_the_player_to_move(impl):
    tree = worked_tree()
    value, move = search(impl, tree.subtree("B"), "B")
    if value != minimax_value(tree, "B", "MIN"):
        pytest.fail(
            f"started at the MIN node B of the worked tree, minimax_search returned the "
            f"value {value!r}. MIN moves there, so {CONVENTION}: for MIN a leaf worth 4 to "
            "MAX is worth −4.",
            pytrace=False,
        )
    assert move in optimal_moves(tree, "B"), f"at B, MIN's best move is B1, not {move!r}"
    state = TIC_TAC_TOE_POSITIONS["o_to_move"]
    value, _ = search(impl, TIC_TAC_TOE, state)
    if value != 1:
        pytest.fail(
            f"in {state}, O is to move and can force a win, so the value is 1, not "
            f"{value!r}. Remember: {CONVENTION}.",
            pytrace=False,
        )


@pytest.mark.parametrize("key", ["win_now", "block", "fork", "o_to_move"])
def test_returns_an_optimal_move(impl, key):
    state = TIC_TAC_TOE_POSITIONS[key]
    _, move = search(impl, TIC_TAC_TOE, state)
    best = optimal_moves(TIC_TAC_TOE, state)
    if move not in best:
        board = TIC_TAC_TOE.render(state).replace("\n", " / ")
        pytest.fail(
            f"in {board} ({TIC_TAC_TOE.to_move(state)} to move) minimax_search chose "
            f"{move!r}, which is not one of the best moves. Return the move whose value is "
            "the one you return, not simply the first move.",
            pytrace=False,
        )


def test_finds_a_forced_win(impl):
    state = TIC_TAC_TOE_POSITIONS["fork"]
    value, move = search(impl, TIC_TAC_TOE, state)
    if value != 1 or move not in optimal_moves(TIC_TAC_TOE, state):
        pytest.fail(
            f"in {' / '.join(state)} X has no win in one move, but it can make two threats "
            f"at once and win two moves later. minimax_search returned ({value!r}, "
            f"{move!r}) — does it search all the way to the end of the game?",
            pytrace=False,
        )


def test_draw_is_worth_zero(impl):
    state = TIC_TAC_TOE_POSITIONS["draw"]
    value, move = search(impl, TIC_TAC_TOE, state)
    assert value == 0, (
        f"with best play from {' / '.join(state)} nobody wins, so the value is 0, not {value!r}"
    )
    assert move in optimal_moves(TIC_TAC_TOE, state), f"{move!r} lets O win"


@pytest.mark.parametrize(
    "rows, value",
    [(["XXX", "OO.", "..."], -1), (["XOX", "XOO", "OXX"], 0)],
    ids=["x_has_won", "full_board"],
)
def test_terminal_state_has_no_move(impl, rows, value):
    state = TIC_TAC_TOE.from_rows(rows)
    found = search(impl, TIC_TAC_TOE, state)
    assert found == (value, None), (
        f"the game is over in {' / '.join(state)}: return ({value}, None) — the utility for "
        f"the player to move ({TIC_TAC_TOE.to_move(state)}) and no move. Got {found!r}"
    )


def test_task_does_not_import_reference_search(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, (
        f"task.py imports {found}: write the search yourself instead of importing the "
        "course's reference version"
    )
