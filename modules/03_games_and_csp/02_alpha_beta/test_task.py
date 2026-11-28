"""Self-check for lesson 3.2: alpha-beta pruning.

Run from the repository root:

    uv run pytest modules/03_games_and_csp/02_alpha_beta

The tests check what every correct alpha-beta does: the same values and moves as
minimax, the leaves it never looks at, and far less work than minimax. A version
that cuts off only at strict inequalities (v > β, v < α) passes too; it prunes a
little less when values tie.
"""

import pytest

from introai.games.examples import (
    TIC_TAC_TOE_POSITIONS,
    alpha_beta_exercise,
    minimax_exercise,
    random_game_tree,
    ties_tree,
    worked_tree,
)
from introai.games.kinarow import TIC_TAC_TOE
from introai.games.reference import alpha_beta_search as reference_alpha_beta
from introai.games.reference import minimax_value
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.testing.games import evaluated_leaves, optimal_moves
from introai.trace import TraceLimitExceeded, record

LIMIT = 200_000  # calls of game.result during one search of a small tree or position
MINIMAX_RESULTS = 549_945  # calls of game.result by minimax from the empty board
STEP_BUDGET = 20_000_000  # lines executed in task.py during one search

TREES = {
    "worked_tree": worked_tree,
    "ties_tree": ties_tree,
    "random_tree": lambda: random_game_tree(3, 4, seed=0),
    "random_odd_tree": lambda: random_game_tree(2, 5, seed=1),
}
PRUNING_TREES = {
    "worked_tree": worked_tree,
    "minimax_exercise": minimax_exercise,
    "random_tree": lambda: random_game_tree(3, 4, seed=2),
}
PRUNING_HINT = (
    "stop the loop as soon as v >= β in a MAX node or v <= α in a MIN node, and pass the "
    "current α and β down to every child"
)


def search(impl, game, state):
    """Call impl.alpha_beta_search(game, state); return its result and the trace."""
    failure = None
    try:
        with (
            record(limit=LIMIT, kinds={"result", "utility"}) as trace,
            step_budget(impl.__file__, STEP_BUDGET),
        ):
            found = impl.alpha_beta_search(game, state)
    except TraceLimitExceeded:
        failure = (
            f"alpha_beta_search made more than {LIMIT} calls of game.result and "
            "game.utility on a small tree or position — does it stop at terminal states?"
        )
    except RecursionError:
        failure = "alpha_beta_search recursed too deeply — does it stop at terminal states?"
    except StepBudgetExceeded:
        failure = "alpha_beta_search ran for too long — is there a loop that never ends?"
    if failure:
        pytest.fail(failure, pytrace=False)
    if not isinstance(found, tuple) or len(found) != 2:
        pytest.fail(
            f"alpha_beta_search must return a pair (value, move), got {found!r}", pytrace=False
        )
    return found, trace


# --- Part A: pruning by hand -----------------------------------------------------------


def test_part_a_pruned_leaves(impl):
    # pytrace=False: no traceback, so pytest cannot print `expected`. Never reveal it.
    tree = alpha_beta_exercise()
    with record(kinds={"utility"}) as trace:
        reference_alpha_beta(tree, tree.initial)
    expected = set(tree.leaves) - set(evaluated_leaves(trace))
    answer = impl.PRUNED_LEAVES
    if answer is None:
        pytest.fail("Part A: fill in PRUNED_LEAVES in task.py", pytrace=False)
    if not isinstance(answer, set | frozenset | list | tuple) or not all(
        isinstance(leaf, str) for leaf in answer
    ):
        pytest.fail(
            'Part A: PRUNED_LEAVES must be a set of leaf names, for example {"K", "L"}',
            pytrace=False,
        )
    unknown = sorted(set(answer) - set(tree.leaves))
    if unknown:
        pytest.fail(
            f"Part A: {', '.join(unknown)} {'is' if len(unknown) == 1 else 'are'} not a leaf "
            "of the exercise tree (leaves are K to V)",
            pytrace=False,
        )
    wrong = len(set(answer) ^ expected)
    if wrong:
        pytest.fail(
            f"Part A: PRUNED_LEAVES is not right yet ({wrong} "
            f"{'leaf is' if wrong == 1 else 'leaves are'} in the wrong place: listed but "
            "looked at, or pruned but missing). Trace the tree again with α and β, "
            "following the rules in the lesson.",
            pytrace=False,
        )


# --- Part B: the same answers as minimax -----------------------------------------------


@pytest.mark.parametrize("name", TREES)
def test_alpha_beta_value_equals_minimax_on_trees(impl, name):
    tree = TREES[name]()
    wrong = []
    for node in tree.children:
        (value, _), _ = search(impl, tree, node)
        if value != minimax_value(tree, node, tree.to_move(node)):
            wrong.append((node, value))
    if wrong:
        node, value = wrong[0]
        pytest.fail(
            f"alpha_beta_search returned a value different from minimax at {len(wrong)} of "
            f"the {len(tree.children)} inner nodes of {name}, for example {value!r} at "
            f"{node!r} (a {tree.to_move(node)} node). The value is for the player to move "
            "at `state` (game.to_move(state)), and pruning must never change it: check whose "
            "utility the leaves get, which bound each node compares v with (β in MAX, α in "
            "MIN) and in what order α and β are passed to the children.",
            pytrace=False,
        )


@pytest.mark.parametrize("key", list(TIC_TAC_TOE_POSITIONS))
def test_alpha_beta_value_equals_minimax_on_positions(impl, key):
    state = TIC_TAC_TOE_POSITIONS[key]
    (value, _), _ = search(impl, TIC_TAC_TOE, state)
    expected = minimax_value(TIC_TAC_TOE, state, TIC_TAC_TOE.to_move(state))
    if value != expected:
        pytest.fail(
            f"in {' / '.join(state)} ({TIC_TAC_TOE.to_move(state)} to move) "
            f"alpha_beta_search returned {value!r}, but minimax gives {expected}. The value "
            "is for the player to move at `state`, and pruning must never change it.",
            pytrace=False,
        )


@pytest.mark.parametrize("key", ["win_now", "block", "fork", "o_to_move"])
def test_alpha_beta_returns_an_optimal_move(impl, key):
    state = TIC_TAC_TOE_POSITIONS[key]
    (_, move), _ = search(impl, TIC_TAC_TOE, state)
    if move not in optimal_moves(TIC_TAC_TOE, state):
        pytest.fail(
            f"in {' / '.join(state)} ({TIC_TAC_TOE.to_move(state)} to move) "
            f"alpha_beta_search chose {move!r}, which is not one of the best moves",
            pytrace=False,
        )


def test_terminal_state_has_no_move(impl):
    state = TIC_TAC_TOE.from_rows(["XXX", "OO.", "..."])
    found, _ = search(impl, TIC_TAC_TOE, state)
    assert found == (-1, None), (
        f"the game is over: return (-1, None) — the utility for O, who is to move, and no "
        f"move. Got {found!r}"
    )


# --- Part B: what it prunes ------------------------------------------------------------


@pytest.mark.parametrize("name", PRUNING_TREES)
def test_alpha_beta_prunes_like_the_lesson(impl, name):
    tree = PRUNING_TREES[name]()
    _, trace = search(impl, tree, tree.initial)
    with record(kinds={"utility"}) as expected_trace:
        reference_alpha_beta(tree, tree.initial)
    seen, expected = set(evaluated_leaves(trace)), set(evaluated_leaves(expected_trace))
    if seen == expected:
        return
    extra, missing = sorted(seen - expected), sorted(expected - seen)
    problems = []
    if extra:
        problems.append(f"it looked at {', '.join(extra)}, which alpha-beta prunes")
    if missing:
        problems.append(f"it never looked at {', '.join(missing)}, which alpha-beta needs")
    pytest.fail(
        f"on {name} alpha_beta_search evaluated the wrong leaves: {'; '.join(problems)}. "
        f"Children are searched in the order of game.actions; {PRUNING_HINT}.",
        pytrace=False,
    )


def test_alpha_beta_accepts_either_rule_on_ties(impl):
    tree = ties_tree()
    _, trace = search(impl, tree, tree.initial)
    seen = set(evaluated_leaves(trace))
    if seen not in ({"B1", "B2", "C1"}, {"B1", "B2", "C1", "C2"}):
        pytest.fail(
            f"on the tree with equal values alpha_beta_search looked at the leaves "
            f"{sorted(seen)}. With the rule v <= α it skips C2; with v < α it looks at all "
            "four leaves. Anything else is not alpha-beta.",
            pytrace=False,
        )


def test_alpha_beta_visits_far_fewer_positions_than_minimax(impl):
    limit = MINIMAX_RESULTS // 2
    try:
        with (
            record(limit=limit, kinds={"result"}),
            step_budget(impl.__file__, STEP_BUDGET),
        ):
            value, move = impl.alpha_beta_search(TIC_TAC_TOE, TIC_TAC_TOE.initial)
    except TraceLimitExceeded:
        pytest.fail(
            f"from the empty board alpha_beta_search called game.result more than {limit} "
            f"times, half of what minimax needs ({MINIMAX_RESULTS}). Is it pruning? To "
            f"prune, {PRUNING_HINT}.",
            pytrace=False,
        )
    except StepBudgetExceeded:
        pytest.fail("alpha_beta_search ran for too long on the empty board", pytrace=False)
    assert value == 0, f"the empty board is worth 0 (a draw), not {value!r}"
    assert move in TIC_TAC_TOE.actions(TIC_TAC_TOE.initial), f"{move!r} is not a legal move"


def test_task_does_not_import_reference_search(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, (
        f"task.py imports {found}: write the search yourself instead of importing the "
        "course's reference version"
    )
