import re
from pathlib import Path

import pytest

from introai.search.reference import bfs
from introai.world.warehouse import RouteProblem, WarehouseMap, render_text

REPO_ROOT = Path(__file__).resolve().parents[1]
SMALL = "#######\n#R..#.#\n#.#...#\n#...#D#\n#######"


def test_from_text_parses_small():
    m = WarehouseMap.from_text(SMALL)
    assert (m.rows, m.cols, m.start, m.dock) == (5, 7, (1, 1), (3, 5))
    assert (1, 4) in m.walls and m.is_free((2, 3)) and not m.is_free((0, 0))
    assert not m.is_free((-1, 0)) and not m.is_free((5, 0))


@pytest.mark.parametrize(
    "variant",
    [
        SMALL.replace("\n", "\r\n"),
        "﻿" + SMALL,
        SMALL.replace("\n", "  \n"),
        SMALL + "\n\n",
        "\n" + SMALL,
    ],
    ids=["crlf", "bom", "trailing-spaces", "trailing-blank-lines", "leading-blank-line"],
)
def test_editor_artifacts_are_tolerated(variant):
    assert WarehouseMap.from_text(variant) == WarehouseMap.from_text(SMALL)


def test_from_file_tolerates_bom(tmp_path):
    f = tmp_path / "m.txt"
    f.write_bytes(("﻿" + SMALL).encode("utf-8"))
    assert WarehouseMap.from_file(f) == WarehouseMap.from_text(SMALL)


@pytest.mark.parametrize(
    "text, message",
    [
        ("", "map is empty"),
        ("\n  \n", "map is empty"),
        ("#####\n#R.D\n#####", "line 2 has 4 characters, expected 5"),
        ("#####\n#RxD#\n#####", "unknown character 'x' at line 2, column 3"),
        ("#####\n#..D#\n#####", "map must contain exactly one 'R' (found 0)"),
        ("#####\n#RDD#\n#####", "map must contain exactly one 'D' (found 2)"),
    ],
)
def test_invalid_maps_raise_clear_errors(text, message):
    with pytest.raises(ValueError, match=re.escape(message)):
        WarehouseMap.from_text(text)


def test_route_problem_actions_and_shortest_path():
    p = RouteProblem(WarehouseMap.from_text(SMALL))
    assert p.initial == (1, 1)
    assert p.actions((1, 1)) == ["E", "S"]
    assert p.result((1, 1), "E") == (1, 2)
    assert p.is_goal((3, 5)) and not p.is_goal((1, 1))
    assert len(bfs(p).solution()) == 6
    assert RouteProblem(p.warehouse, ("W", "S", "E", "N")).actions((1, 1)) == ["S", "E"]


def test_route_problem_rejects_blocked_move():
    p = RouteProblem(WarehouseMap.from_text(SMALL))
    with pytest.raises(ValueError):
        p.result((1, 1), "N")


def test_render_text_marks_path_and_expanded():
    m = WarehouseMap.from_text(SMALL)
    assert render_text(m, path=[(1, 1), (1, 2)], expanded=[(2, 1)]) == (
        "#######\n#R*.#.#\n#o#...#\n#...#D#\n#######"
    )


def test_render_text_without_marks_round_trips():
    assert render_text(WarehouseMap.from_text(SMALL)) == SMALL


def test_bundled_maps_load_and_are_solvable():
    for name in ("small", "aisles", "open_floor", "parcels", "congested"):
        m = WarehouseMap.from_file(REPO_ROOT / "data" / "maps" / f"{name}.txt")
        assert m.rows <= 15 and m.cols <= 30
        assert bfs(RouteProblem(m)) is not None
    small = WarehouseMap.from_file(REPO_ROOT / "data" / "maps" / "small.txt")
    assert small == WarehouseMap.from_text(SMALL)


def test_from_file_explains_a_wrong_encoding(tmp_path):
    f = tmp_path / "m.txt"
    f.write_text(SMALL, encoding="utf-16")  # e.g. Notepad "UTF-16 LE" or PowerShell 5.1 ">"
    with pytest.raises(ValueError, match="save the map as UTF-8"):
        WarehouseMap.from_file(f)


PARCELS = "#######\n#R.P#P#\n#.#...#\n#..P#D#\n#######"


def test_parcels_are_parsed():
    m = WarehouseMap.from_text(PARCELS)
    assert m.parcels == {(1, 3), (1, 5), (3, 3)}
    assert m.is_free((1, 3))


def test_maps_without_parcels_have_none():
    assert WarehouseMap.from_text(SMALL).parcels == frozenset()


def test_with_parcels_places_and_validates():
    m = WarehouseMap.from_text(SMALL)
    assert m.with_parcels([(2, 3)]).parcels == {(2, 3)}
    assert m.with_parcels([(2, 3)]).walls == m.walls
    with pytest.raises(
        ValueError, match=re.escape("cannot place a parcel on an obstacle at (0, 0)")
    ):
        m.with_parcels([(0, 0)])
    with pytest.raises(ValueError, match=re.escape("on an obstacle at (9, 9)")):
        m.with_parcels([(9, 9)])
    with pytest.raises(ValueError, match="cannot place a parcel on the robot's start"):
        m.with_parcels([m.start])


def test_render_text_round_trips_parcels():
    assert render_text(WarehouseMap.from_text(PARCELS)) == PARCELS


def test_parcels_map_file():
    path = REPO_ROOT / "data" / "maps" / "parcels.txt"
    assert WarehouseMap.from_file(path) == WarehouseMap.from_text(PARCELS)


COSTLY = "#####\n#R~D#\n#####"


def test_slow_zones_are_parsed_and_cost_three():
    m = WarehouseMap.from_text(COSTLY)
    assert m.slow == {(1, 2)} and m.is_free((1, 2))
    assert (m.cost((1, 2)), m.cost((1, 3)), m.cost((1, 1))) == (3, 1, 1)


def test_maps_without_slow_zones_have_none():
    assert WarehouseMap.from_text(SMALL).slow == frozenset()


def test_route_problem_uses_cell_costs():
    p = RouteProblem(WarehouseMap.from_text(COSTLY))
    assert p.action_cost((1, 1), "E", (1, 2)) == 3
    assert p.action_cost((1, 2), "E", (1, 3)) == 1


def test_render_text_round_trips_slow_zones():
    assert render_text(WarehouseMap.from_text(COSTLY)) == COSTLY
    assert (
        render_text(WarehouseMap.from_text(COSTLY), path=[(1, 1), (1, 2)]) == "#####\n#R*D#\n#####"
    )


def test_congested_map_has_slow_zones():
    m = WarehouseMap.from_file(REPO_ROOT / "data" / "maps" / "congested.txt")
    assert m.slow and m.rows <= 15 and m.cols <= 30


def test_depot_map_separates_the_strategies():
    from introai.search.reference import a_star, bfs, dfs, greedy_best_first, ucs
    from introai.trace import record
    from introai.world.reference import manhattan

    depot = WarehouseMap.from_file(Path(__file__).resolve().parents[1] / "data/maps/depot.txt")
    assert depot.slow, "the depot has slow zones"

    def h(cell):
        return manhattan(cell, depot.dock)

    results = {}
    for name, search in [
        ("bfs", bfs),
        ("dfs", dfs),
        ("ucs", ucs),
        ("greedy", lambda p: greedy_best_first(p, h)),
        ("astar", lambda p: a_star(p, h)),
    ]:
        with record(kinds={"expand"}) as trace:
            node = search(RouteProblem(depot))
        results[name] = (node.path_cost, len(node.solution()), len(trace.of_kind("expand")))
    cost = {name: value[0] for name, value in results.items()}
    assert cost["bfs"] > cost["ucs"], results
    assert cost["greedy"] > cost["ucs"], results
    assert cost["astar"] == cost["ucs"] and results["astar"][2] < results["ucs"][2], results
    assert results["dfs"][1] == max(steps for _, steps, _ in results.values()), results
