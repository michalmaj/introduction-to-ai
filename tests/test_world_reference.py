from pathlib import Path

import pytest

from introai.search.reference import bfs
from introai.world.reference import ParcelPickupProblem
from introai.world.warehouse import WarehouseMap

MAP_DIR = Path(__file__).resolve().parents[1] / "data" / "maps"
MAP = WarehouseMap.from_file(MAP_DIR / "parcels.txt")
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


def test_reference_free_neighbours():
    from introai.world.reference import free_neighbours

    small = WarehouseMap.from_file(MAP_DIR / "small.txt")
    assert free_neighbours(small, (2, 3)) == [(1, 3), (2, 4), (3, 3)]
    assert free_neighbours(WarehouseMap.from_text("R..\n.#.\n..D"), (0, 0)) == [(0, 1), (1, 0)]


def test_reference_manhattan():
    from introai.world.reference import manhattan

    assert manhattan((1, 1), (3, 5)) == 6 and manhattan((3, 5), (1, 1)) == 6
    assert manhattan((2, 2), (2, 2)) == 0


def test_congested_map_shows_why_costs_matter():
    from introai.search.reference import a_star, ucs
    from introai.trace import record
    from introai.world.reference import manhattan
    from introai.world.warehouse import RouteProblem

    problem = RouteProblem(WarehouseMap.from_file(MAP_DIR / "congested.txt"))
    fewest_steps, cheapest = bfs(problem), ucs(problem)
    assert len(fewest_steps.solution()) < len(cheapest.solution())
    assert fewest_steps.path_cost > cheapest.path_cost
    with record(kinds={"expand"}) as by_ucs:
        ucs(problem)
    with record(kinds={"expand"}) as by_a_star:
        found = a_star(problem, lambda cell: manhattan(cell, problem.warehouse.dock))
    assert found.path_cost == cheapest.path_cost
    assert len(by_a_star.events) < len(by_ucs.events)
