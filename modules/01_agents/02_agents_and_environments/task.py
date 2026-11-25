"""Lesson 1.2: agents and environments.

Read the lesson first: README.pl.md (Polish) or README.md (English) in this directory.

Part A: classify the two warehouse variants described in the lesson.
Part B: implement reflex_agent().

Check your work from the repository root:

    uv run pytest modules/01_agents/02_agents_and_environments
"""

from introai.agents import Percept

# ---------------------------------------------------------------------------------------
# Part A: the properties of variant 1 and variant 2 (section "Two warehouse variants").
# Replace every None with one of the two values given in the comment.
# ---------------------------------------------------------------------------------------

VARIANT_1: dict[str, str | None] = {
    "observable": None,  # "fully" or "partially"
    "agents": None,  # "single" or "multi"
    "deterministic": None,  # "deterministic" or "stochastic"
    "episodic": None,  # "episodic" or "sequential"
    "static": None,  # "static" or "dynamic"
    "discrete": None,  # "discrete" or "continuous"
}

VARIANT_2: dict[str, str | None] = {
    "observable": None,  # "fully" or "partially"
    "agents": None,  # "single" or "multi"
    "deterministic": None,  # "deterministic" or "stochastic"
    "episodic": None,  # "episodic" or "sequential"
    "static": None,  # "static" or "dynamic"
    "discrete": None,  # "discrete" or "continuous"
}


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def reflex_agent(percept: Percept) -> str:
    """A simple reflex agent for the parcel world.

    ``percept.parcel_here`` says whether a parcel lies on the robot's cell;
    ``percept.free`` lists the free directions in the order N, E, S, W.
    Return one of "N", "E", "S", "W", "PICK", "WAIT", following the three rules
    in the lesson.
    """
    raise NotImplementedError(
        'TODO: implement reflex_agent in task.py (or set IMPLEMENTATION = "reference" in '
        "the notebook's first cell)"
    )
