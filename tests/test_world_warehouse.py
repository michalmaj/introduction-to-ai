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
    for name in ("small", "aisles", "open_floor"):
        m = WarehouseMap.from_file(REPO_ROOT / "data" / "maps" / f"{name}.txt")
        assert m.rows <= 15 and m.cols <= 30
        assert bfs(RouteProblem(m)) is not None
    small = WarehouseMap.from_file(REPO_ROOT / "data" / "maps" / "small.txt")
    assert small == WarehouseMap.from_text(SMALL)
