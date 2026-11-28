"""Self-check for lesson 3.3: evaluation functions and depth limits.

Run from the repository root:

    uv run pytest modules/03_games_and_csp/03_evaluation_functions

The search is checked like alpha-beta in lesson 3.2, plus the depth limit: where it
stops, what it evaluates and what it still scores with the utility. Your evaluation
is checked by its range and by a match: there is no single correct evaluation, but a
good one must beat a player who has none.
"""

import numbers
import random

import pytest

from introai.games.examples import TIC_TAC_TOE_POSITIONS, cutoff_tree, tree_evaluation
from introai.games.kinarow import TIC_TAC_TOE, KInARow
from introai.games.players import MATCH_OPENINGS, alpha_beta_player, match
from introai.games.reference import h_alpha_beta_search as reference_h_search
from introai.games.reference import minimax_value, zero_evaluation
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.games import optimal_moves
from introai.trace import TraceLimitExceeded, record

LIMIT = 200_000  # calls of game.result during one search
STEP_BUDGET = 50_000_000  # lines executed in task.py during one call
BOARD = KInARow(5, 5, 4)
EVAL_POSITIONS = [("X..", ".O.", "..."), ("X.O", ".X.", "..."), ("X..", ".O.", "..X")]
WIN_IN_ONE = ("OO...", "O....", ".....", "XXX..", ".....")


def search(impl, game, state, depth, evaluate, limit=LIMIT, hint=""):
    """Call impl.h_alpha_beta_search; return its result and the trace."""
    failure = None
    try:
        with (
            record(limit=limit, kinds={"result", "utility"}) as trace,
            step_budget(impl.__file__, STEP_BUDGET),
        ):
            found = impl.h_alpha_beta_search(game, state, depth, evaluate)
    except TraceLimitExceeded:
        failure = (
            f"h_alpha_beta_search made more than {limit} calls of game.result and "
            f"game.utility {hint}— does it stop when the depth runs out?"
        )
    except RecursionError:
        failure = "h_alpha_beta_search recursed too deeply — does it stop at the depth limit?"
    except StepBudgetExceeded:
        failure = "h_alpha_beta_search ran for too long — is there a loop that never ends?"
    if failure:
        pytest.fail(failure, pytrace=False)
    if not isinstance(found, tuple) or len(found) != 2:
        pytest.fail(
            f"h_alpha_beta_search must return a pair (value, move), got {found!r}",
            pytrace=False,
        )
    return found, trace


def call_evaluate(impl, game, state, player):
    """Call impl.evaluate and turn crashes into hints."""
    try:
        with step_budget(impl.__file__, STEP_BUDGET):
            return impl.evaluate(game, state, player)
    except NotImplementedError:
        pytest.fail("evaluate is not written yet", pytrace=False)
    except StepBudgetExceeded:
        pytest.fail("evaluate ran for too long — is there a loop that never ends?", pytrace=False)
    except Exception as error:  # the student's code may fail in any way
        board = " / ".join(state)
        pytest.fail(
            f"evaluate(game, {board!r}, {player!r}) raised {type(error).__name__}: {error}",
            pytrace=False,
        )


def open_line_difference(state):
    """The Part A evaluation: lines still open for X minus lines still open for O."""
    x_open = sum("O" not in {state[r][c] for r, c in line} for line in TIC_TAC_TOE.lines)
    o_open = sum("X" not in {state[r][c] for r, c in line} for line in TIC_TAC_TOE.lines)
    return x_open - o_open


# --- Part A: evaluating by hand --------------------------------------------------------


def test_part_a_eval_values(impl):
    # pytrace=False: no traceback, so pytest cannot print `expected`. Never reveal it.
    values, name = impl.EVAL_VALUES, "EVAL_VALUES"
    expected = [open_line_difference(state) for state in EVAL_POSITIONS]
    if values is None:
        pytest.fail(f"Part A: fill in {name} in task.py", pytrace=False)
    if (
        not isinstance(values, list | tuple)
        or len(values) != len(expected)
        or not all(isinstance(v, int) and not isinstance(v, bool) for v in values)
    ):
        pytest.fail(
            f"Part A: {name} must be a list of {len(expected)} whole numbers, one per "
            "position, for example [0, 0, 0]",
            pytrace=False,
        )
    wrong = sum(v != e for v, e in zip(values, expected))
    if wrong:
        pytest.fail(
            f"Part A: {wrong} of the {len(expected)} values in {name} are not right yet. "
            "Count the lines without an O (open for X) and the lines without an X (open "
            "for O) — all 8 lines, empty ones too.",
            pytrace=False,
        )


def test_part_a_depth_one_move(impl):
    state = TIC_TAC_TOE_POSITIONS["block"]
    move = impl.DEPTH_ONE_MOVE
    if move is None:
        pytest.fail("Part A: fill in DEPTH_ONE_MOVE in task.py", pytrace=False)
    if not isinstance(move, tuple) or move not in TIC_TAC_TOE.actions(state):
        pytest.fail(
            f"Part A: DEPTH_ONE_MOVE must be an empty cell (row, col) of the position, one "
            f"of {TIC_TAC_TOE.actions(state)}",
            pytrace=False,
        )

    def scaled(game, s, player):
        e = open_line_difference(s) / 9
        return e if player == "X" else -e

    _, expected = reference_h_search(TIC_TAC_TOE, state, 1, scaled)
    if move != expected:
        pytest.fail(
            "Part A: DEPTH_ONE_MOVE is not right yet. Compute e for the position after each "
            "of X's moves and take the move with the largest e.",
            pytrace=False,
        )


# --- Part B: the depth-limited search --------------------------------------------------


@pytest.mark.parametrize("depth", [1, 2, 3])
def test_h_search_values_on_a_tree(impl, depth):
    tree = cutoff_tree()
    (value, move), _ = search(impl, tree, tree.initial, depth, tree_evaluation)
    expected = reference_h_search(tree, tree.initial, depth, tree_evaluation)
    if (value, move) != expected:
        pytest.fail(
            f"on a tree three moves deep with estimates at the inner nodes, "
            f"h_alpha_beta_search(depth={depth}) returned ({value!r}, {move!r}). Check that "
            f"a node {depth} moves below the start gets evaluate(game, node, player) with "
            "the player to move at the START (or the negamax sign), and that each move "
            "lowers the remaining depth by exactly 1.",
            pytrace=False,
        )


def test_h_search_evaluates_only_at_the_cutoff(impl):
    tree = cutoff_tree()
    evaluated = []

    def evaluate(game, state, player):
        evaluated.append(state)
        return tree_evaluation(game, state, player)

    _, trace = search(impl, tree, tree.initial, 1, evaluate)
    leaves = [event.data["state"] for event in trace.of_kind("utility")]
    if sorted(evaluated) != ["B", "C"] or leaves:
        pytest.fail(
            f"with depth 1 the search should evaluate exactly the two children of the "
            f"root, B and C, and never reach a leaf. It evaluated {evaluated} and asked for "
            f"the utility of {leaves}.",
            pytrace=False,
        )


def test_h_search_takes_an_immediate_win(impl):
    state = BOARD.from_rows(WIN_IN_ONE)
    found, _ = search(impl, BOARD, state, 1, zero_evaluation)
    if found != (1, (3, 3)):
        pytest.fail(
            f"X wins at once by playing (3, 3), but h_alpha_beta_search(depth=1) with an "
            f"evaluation that always returns 0 gave {found!r}. A terminal state gets its "
            "utility, even at the depth limit: test is_terminal before the depth.",
            pytrace=False,
        )


@pytest.mark.parametrize("key", list(TIC_TAC_TOE_POSITIONS))
def test_h_search_with_full_depth_equals_minimax(impl, key):
    state = TIC_TAC_TOE_POSITIONS[key]
    (value, move), _ = search(impl, TIC_TAC_TOE, state, 9, zero_evaluation)
    expected = minimax_value(TIC_TAC_TOE, state, TIC_TAC_TOE.to_move(state))
    if value != expected or move not in optimal_moves(TIC_TAC_TOE, state):
        pytest.fail(
            f"with depth 9 nothing is cut off, so the search is plain alpha-beta. In "
            f"{' / '.join(state)} ({TIC_TAC_TOE.to_move(state)} to move) it returned "
            f"({value!r}, {move!r}), but minimax gives the value {expected}. The value is "
            "for the player to move at `state` (game.to_move(state)): score leaves and "
            "estimates for that player.",
            pytrace=False,
        )


def test_h_search_stops_at_the_depth_on_a_large_board(impl):
    (_, move), _ = search(
        impl,
        BOARD,
        BOARD.initial,
        2,
        zero_evaluation,
        limit=1_000,
        hint="from the empty 5 × 5 board with depth 2 (two moves need at most 625) ",
    )
    assert move in BOARD.actions(BOARD.initial), f"{move!r} is not a legal first move"


# --- Part B: the evaluation function ---------------------------------------------------


def playout_positions(count=200, seed=0):
    """Non-terminal 5 × 5 positions reached by seeded random moves."""
    rng = random.Random(seed)
    positions = []
    while len(positions) < count:
        state = BOARD.initial
        for _ in range(rng.randrange(1, 16)):
            state = BOARD.result(state, rng.choice(BOARD.actions(state)))
            if BOARD.is_terminal(state):
                break
        if not BOARD.is_terminal(state):
            positions.append(state)
    return positions


def test_evaluation_stays_between_loss_and_win(impl):
    for state in playout_positions():
        for player in BOARD.players:
            e = call_evaluate(impl, BOARD, state, player)
            board = " / ".join(state)
            if isinstance(e, bool) or not isinstance(e, numbers.Real):
                pytest.fail(
                    f"evaluate(game, {board!r}, {player!r}) returned {e!r}: an evaluation "
                    "must be a number",
                    pytrace=False,
                )
            if not -1 <= e <= 1:
                pytest.fail(
                    f"evaluate(game, {board!r}, {player!r}) returned {e}, outside [−1, 1]. "
                    "A position that is not over must not look better than a win (1) or "
                    "worse than a loss (−1): squeeze your score, e.g. x / (1 + |x|).",
                    pytrace=False,
                )


ONE_SIDED = [
    # (rows, the strong player): three in a row with both ends free against scattered marks
    (("O...O", ".....", ".XXX.", ".....", "....O"), "X"),
    (("X...X", ".....", ".OOO.", ".....", "X...."), "O"),
]


@pytest.mark.parametrize("rows, strong", ONE_SIDED, ids=["x_is_ahead", "o_is_ahead"])
def test_evaluation_is_for_the_given_player(impl, rows, strong):
    state = BOARD.from_rows(rows)
    weak = "O" if strong == "X" else "X"
    mine = call_evaluate(impl, BOARD, state, strong)
    theirs = call_evaluate(impl, BOARD, state, weak)
    if not (isinstance(mine, numbers.Real) and isinstance(theirs, numbers.Real)):
        pytest.fail("evaluate must return a number", pytrace=False)
    if not (mine > 0 and mine > theirs):
        pytest.fail(
            f"in {' / '.join(rows)} {strong} has three in a row with both ends free and "
            f"{weak} only scattered marks, so the position is good for {strong}. But "
            f"evaluate(game, state, {strong!r}) returned {mine} and evaluate(game, state, "
            f"{weak!r}) returned {theirs}. Score the position for `player`, whoever it is: "
            "Part A's e is always from X's side, your evaluate is not.",
            pytrace=False,
        )


def test_evaluation_beats_a_player_without_one(impl):
    def evaluate(game, state, player):
        return call_evaluate(impl, game, state, player)

    try:
        table = match(BOARD, alpha_beta_player(2, evaluate), alpha_beta_player(2, zero_evaluation))
    except TypeError as error:
        pytest.fail(
            f"the match stopped: {error}. Does evaluate always return a number?",
            pytrace=False,
        )
    games = 2 * len(MATCH_OPENINGS)
    wins, draws, losses = table["win"], table["draw"], table["loss"]
    if wins < games // 2 or wins <= losses:
        pytest.fail(
            f"with your evaluation, depth-2 alpha-beta won {wins}, drew {draws} and lost "
            f"{losses} of {games} games against the same search with an evaluation that "
            f"always returns 0. To pass, win at least {games // 2} games and more than you "
            "lose. Is the sign right (good for `player` means positive)? Does it reward "
            "lines with more of the player's marks?",
            pytrace=False,
        )


def test_task_does_not_import_reference_search(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, (
        f"task.py imports {found}: write the search and the evaluation yourself instead of "
        "importing the course's reference versions"
    )
