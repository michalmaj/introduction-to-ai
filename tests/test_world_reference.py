from pathlib import Path

import pytest

from introai.search.reference import bfs
from introai.world.reference import ParcelPickupProblem
from introai.world.warehouse import WarehouseMap

MAP = WarehouseMap.from_file(Path(__file__).resolve().parents[1] / "data" / "maps" / "parcels.txt")
A, B, C = (1, 3), (1, 5), (3, 3)


def test_initial_state():
    assert ParcelPickupProblem(MAP).initial == ((1, 1), frozenset({A, B, C}))


def test_actions_are_moves_then_pick():
    problem = ParcelPickupProblem(MAP)
    assert problem.actions(((1, 1), frozenset({A}))) == ["E", "S"]
    assert problem.actions((A, frozenset({A, C}))) == ["S", "W", "PICK"]
    assert problem.actions((A, frozenset({C}))) == ["S", "W"]


def test_result():
    problem = ParcelPickupProblem(MAP)
    assert problem.result(((1, 1), frozenset({A})), "E") == ((1, 2), frozenset({A}))
    assert problem.result((A, frozenset({A, C})), "PICK") == (A, frozenset({C}))
    with pytest.raises(ValueError):
        problem.result(((1, 1), frozenset({A})), "N")
    with pytest.raises(ValueError):
        problem.result(((1, 1), frozenset({A})), "PICK")


def test_is_goal():
    problem = ParcelPickupProblem(MAP)
    assert problem.is_goal(((2, 4), frozenset()))
    assert not problem.is_goal(((2, 4), frozenset({A})))


@pytest.mark.parametrize(
    "parcels, optimal",
    [([A], 3), ([A, C], 6), ([A, B, C], 11)],
)
def test_bfs_finds_the_hand_computed_optimum(parcels, optimal):
    problem = ParcelPickupProblem(MAP.with_parcels(parcels))
    assert len(bfs(problem).solution()) == optimal
