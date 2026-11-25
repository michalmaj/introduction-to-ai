from itertools import combinations
from pathlib import Path

import pytest

from introai.agents import Percept, run_episode
from introai.agents.reference import ENVIRONMENT_PROPERTIES, ModelBasedAgent, reflex_agent
from introai.world.warehouse import WarehouseMap

MAP = WarehouseMap.from_file(Path(__file__).resolve().parents[1] / "data" / "maps" / "parcels.txt")
DIRECTIONS = ("N", "E", "S", "W")
ALL_FREE_SETS = [combo for size in range(5) for combo in combinations(DIRECTIONS, size)]


@pytest.mark.parametrize("parcel_here", [False, True])
@pytest.mark.parametrize("free", ALL_FREE_SETS)
def test_reflex_agent_rules(parcel_here, free):
    action = reflex_agent(Percept(parcel_here, free))
    if parcel_here:
        assert action == "PICK"
    elif free:
        assert action == free[0]
    else:
        assert action == "WAIT"


def test_reflex_agent_loops_after_the_first_parcel():
    result = run_episode(reflex_agent, MAP, max_steps=200)
    assert result.collected == 1 and result.steps == 200
    assert set(result.trajectory[-10:]) == {(1, 3), (2, 3)}


def test_model_based_agent_collects_everything():
    result = run_episode(ModelBasedAgent(), MAP, max_steps=200)
    assert result.collected == 3
    assert result.score > run_episode(reflex_agent, MAP, max_steps=200).score


def test_model_based_agent_waits_when_boxed_in():
    assert ModelBasedAgent()(Percept(False, ())) == "WAIT"


def test_environment_properties():
    values = {
        "observable": {"fully", "partially"},
        "agents": {"single", "multi"},
        "deterministic": {"deterministic", "stochastic"},
        "episodic": {"episodic", "sequential"},
        "static": {"static", "dynamic"},
        "discrete": {"discrete", "continuous"},
    }
    assert set(ENVIRONMENT_PROPERTIES) == {"variant_1", "variant_2"}
    for answers in ENVIRONMENT_PROPERTIES.values():
        assert set(answers) == set(values)
        assert all(answers[key] in allowed for key, allowed in values.items())
    assert ENVIRONMENT_PROPERTIES["variant_1"]["observable"] == "partially"
    assert ENVIRONMENT_PROPERTIES["variant_2"]["agents"] == "multi"
