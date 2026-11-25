"""Mutant: tries the directions in the order W, S, E, N instead of N, E, S, W.

Violated requirement: rule 2, the first free direction in the order N, E, S, W.
Common mistake in the lesson: "The wrong order of directions".
"""

from introai.agents import Percept

CAUGHT_BY = ("test_reflex_agent_follows_priority",)

# ---------------------------------------------------------------------------------------
# Part A: the properties of the two variants.
# ---------------------------------------------------------------------------------------

VARIANT_1: dict[str, str | None] = {
    "observable": "partially",  # the robot senses only its cell and its four neighbours
    "agents": "single",  # it works alone
    "deterministic": "deterministic",  # every action has exactly one outcome
    "episodic": "sequential",  # what it does now changes what is left to do later
    "static": "static",  # nothing changes while the robot decides
    "discrete": "discrete",  # cells, steps and a handful of actions
}

VARIANT_2: dict[str, str | None] = {
    "observable": "fully",  # a camera shows the whole hall every step
    "agents": "multi",  # other robots work in the same hall
    "deterministic": "stochastic",  # wheels slip: a move may fail
    "episodic": "sequential",
    "static": "dynamic",  # the other robots move while ours decides
    "discrete": "discrete",
}


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def reflex_agent(percept: Percept) -> str:
    """A simple reflex agent: three condition-action rules on the current percept."""
    if percept.parcel_here:  # rule 1
        return "PICK"
    for direction in ("W", "S", "E", "N"):  # BUG: reversed priority
        if direction in percept.free:
            return direction
    return "WAIT"  # rule 3
