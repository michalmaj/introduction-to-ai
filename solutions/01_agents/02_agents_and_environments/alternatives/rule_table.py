"""Alternative: the three rules as an explicit condition-action table."""

from introai.agents import Percept

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
    rules = [
        (lambda p: p.parcel_here, lambda p: "PICK"),
        (lambda p: bool(p.free), lambda p: p.free[0]),
        (lambda p: True, lambda p: "WAIT"),
    ]
    for condition, action in rules:
        if condition(percept):
            return action(percept)
    raise AssertionError("the last rule always applies")
