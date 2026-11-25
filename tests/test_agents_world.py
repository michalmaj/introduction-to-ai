import re
from pathlib import Path

import pytest

from introai.agents import (
    ACTIONS,
    EpisodeResult,
    ParcelWorld,
    Percept,
    random_agent,
    run_episode,
)
from introai.world.warehouse import WarehouseMap

MAP = WarehouseMap.from_file(Path(__file__).resolve().parents[1] / "data" / "maps" / "parcels.txt")


def test_actions():
    assert ACTIONS == ("N", "E", "S", "W", "PICK", "WAIT")


def test_initial_state_and_percept():
    world = ParcelWorld(MAP)
    assert world.robot == (1, 1)
    assert world.parcels == {(1, 3), (1, 5), (3, 3)}
    assert world.percept() == Percept(False, ("E", "S"))
    assert (world.score, world.steps, world.collected) == (0, 0, 0)


def test_move_and_bump():
    world = ParcelWorld(MAP)
    world.step("E")
    assert world.robot == (1, 2) and world.score == -1
    world.step("N")  # a wall: the robot bumps and stays
    assert world.robot == (1, 2) and world.score == -2 and world.steps == 2


def test_pick_collects_a_parcel_once():
    world = ParcelWorld(MAP)
    world.step("E")
    world.step("E")
    assert world.percept().parcel_here
    world.step("PICK")
    assert world.collected == 1 and (1, 3) not in world.parcels and world.score == -3 + 10
    world.step("PICK")  # nothing left here
    assert world.collected == 1 and world.score == -4 + 10


def test_wait_costs_one_point():
    world = ParcelWorld(MAP)
    world.step("WAIT")
    assert world.robot == (1, 1) and world.score == -1


def test_unknown_action_is_rejected():
    world = ParcelWorld(MAP)
    message = "unknown action 'UP'; expected one of N, E, S, W, PICK, WAIT"
    with pytest.raises(ValueError, match=re.escape(message)):
        world.step("UP")


def test_world_does_not_change_the_map():
    world = ParcelWorld(MAP)
    for action in ("E", "E", "PICK"):
        world.step(action)
    assert MAP.parcels == {(1, 3), (1, 5), (3, 3)}


def test_done_when_no_parcels_left():
    world = ParcelWorld(MAP.with_parcels([(1, 2)]))
    assert not world.done
    world.step("E")
    world.step("PICK")
    assert world.done


def test_run_episode_stops_when_done():
    def agent(percept):
        return "PICK" if percept.parcel_here else "E"

    result = run_episode(agent, MAP.with_parcels([(1, 3)]))
    assert result == EpisodeResult(
        score=10 - 3, steps=3, collected=1, trajectory=((1, 1), (1, 2), (1, 3), (1, 3))
    )


def test_run_episode_stops_at_max_steps():
    result = run_episode(lambda percept: "WAIT", MAP, max_steps=5)
    assert result.steps == 5 and len(result.trajectory) == 6 and result.score == -5


def test_run_episode_rejects_an_invalid_agent_answer():
    with pytest.raises(ValueError, match="unknown action None"):
        run_episode(lambda percept: None, MAP)


def test_random_agent_is_reproducible():
    first = run_episode(random_agent(0), MAP, max_steps=50)
    again = run_episode(random_agent(0), MAP, max_steps=50)
    other = run_episode(random_agent(1), MAP, max_steps=50)
    assert first == again and first != other
