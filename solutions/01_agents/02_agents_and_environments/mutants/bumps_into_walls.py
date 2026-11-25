"""Mutant: ignores which directions are free and always drives north.

Violated requirement: rule 2, move only in a free direction.
Common mistake in the lesson: "Driving into walls".
"""

from introai.agents import Percept

CAUGHT_BY = ("test_reflex_agent_never_bumps",)

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
    if percept.free:
        return "N"  # BUG: north even when north is blocked
    return "WAIT"  # rule 3
