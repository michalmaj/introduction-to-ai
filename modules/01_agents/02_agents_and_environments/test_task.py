"""Self-check for lesson 1.2: agents and environments.

Run from the repository root:

    uv run pytest modules/01_agents/02_agents_and_environments
"""

from itertools import combinations

import pytest

from introai.agents import ACTIONS, Percept
from introai.agents.reference import ENVIRONMENT_PROPERTIES
from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget

DIRECTIONS = ("N", "E", "S", "W")
FREE_SETS = [combo for size in range(5) for combo in combinations(DIRECTIONS, size)]
ALL_PERCEPTS = [Percept(parcel, free) for parcel in (False, True) for free in FREE_SETS]
ALLOWED = {
    "observable": ("fully", "partially"),
    "agents": ("single", "multi"),
    "deterministic": ("deterministic", "stochastic"),
    "episodic": ("episodic", "sequential"),
    "static": ("static", "dynamic"),
    "discrete": ("discrete", "continuous"),
}


def act(impl, percept):
    """Ask the student's agent for an action; turn endless loops into a hint."""
    function = impl.reflex_agent
    failure = None
    try:
        with step_budget(function.__code__.co_filename, 100_000):
            action = function(percept)
    except StepBudgetExceeded:
        failure = "reflex_agent ran for too long — it should answer a percept immediately"
    if failure:
        pytest.fail(failure, pytrace=False)
    return action


# --- Part A: properties of the two environment variants --------------------------------


def check_variant(value, name, expected):
    if not isinstance(value, dict):
        pytest.fail(f"Part A: {name} must be a dict like the one in task.py", pytrace=False)
    missing = [key for key in ALLOWED if value.get(key) is None]
    if missing:
        pytest.fail(f"Part A: fill in {name}[{missing[0]!r}] in task.py", pytrace=False)
    for key, allowed in ALLOWED.items():
        if value[key] not in allowed:
            pytest.fail(
                f"Part A: {name}[{key!r}] must be one of {', '.join(map(repr, allowed))}",
                pytrace=False,
            )
    wrong = sum(value[key] != expected[key] for key in ALLOWED)
    if wrong:
        # Only the number of wrong answers: naming them would give the answers away.
        pytest.fail(
            f"Part A: {name} has {wrong} wrong answer(s) out of {len(ALLOWED)}. Re-read the "
            "description of the variant and the definitions of the properties in the lesson.",
            pytrace=False,
        )


def test_part_a_variant_1(impl):
    check_variant(impl.VARIANT_1, "VARIANT_1", ENVIRONMENT_PROPERTIES["variant_1"])


def test_part_a_variant_2(impl):
    check_variant(impl.VARIANT_2, "VARIANT_2", ENVIRONMENT_PROPERTIES["variant_2"])


# --- Part B: the reflex agent ----------------------------------------------------------


def expected_action(percept):
    if percept.parcel_here:
        return "PICK"
    return percept.free[0] if percept.free else "WAIT"


def test_reflex_agent_returns_a_valid_action(impl):
    for percept in ALL_PERCEPTS:
        action = act(impl, percept)
        assert action in ACTIONS, f"for {percept} the agent returned {action!r}, not an action"


def test_reflex_agent_picks_up_parcels(impl):
    for percept in ALL_PERCEPTS:
        if percept.parcel_here:
            assert act(impl, percept) == "PICK", (
                f"for {percept} a parcel lies right here: rule 1 says PICK"
            )


def test_reflex_agent_never_bumps(impl):
    for percept in ALL_PERCEPTS:
        action = act(impl, percept)
        if action in DIRECTIONS:
            assert action in percept.free, (
                f"for {percept} the agent drove {action} into an obstacle: move only in a free "
                "direction"
            )


def test_reflex_agent_waits_when_boxed_in(impl):
    assert act(impl, Percept(False, ())) == "WAIT", (
        "with no parcel and no free direction, rule 3 says WAIT"
    )


def test_reflex_agent_follows_priority(impl):
    for percept in ALL_PERCEPTS:
        for attempt in range(2):  # a reflex agent gives the same answer every time
            action = act(impl, percept)
            assert action == expected_action(percept), (
                f"for {percept} the rules give {expected_action(percept)!r}, the agent "
                f"returned {action!r} (attempt {attempt + 1}); free directions are tried in the "
                "order N, E, S, W"
            )


def test_task_does_not_import_reference(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, f"task.py imports {found}: write the agent and the answers yourself"
