"""Self-check for lesson 0.1: setup and the warehouse world.

Run from the repository root:

    uv run pytest modules/00_start/01_setup
"""

from pathlib import Path

import pytest

from introai.testing.ast_checks import find_reference_imports
from introai.testing.budget import StepBudgetExceeded, step_budget
from introai.world.warehouse import WarehouseMap

MAPS = Path(__file__).resolve().parents[3] / "data" / "maps"
SMALL = WarehouseMap.from_file(MAPS / "small.txt")
NO_BORDER = WarehouseMap.from_text("R..\n.#.\n..D")  # a map whose edges are free floor


def neighbours(impl, warehouse, cell):
    """Call the student's free_neighbours, turning endless loops and wrong types into hints."""
    function = impl.free_neighbours
    failure = None
    try:
        with step_budget(function.__code__.co_filename, 100_000):
            result = function(warehouse, cell)
    except StepBudgetExceeded:
        failure = "free_neighbours ran for too long — is there a loop that never ends?"
    if failure:
        pytest.fail(failure, pytrace=False)
    if not isinstance(result, list):
        pytest.fail(
            f"free_neighbours must return a list of cells, got {type(result).__name__}",
            pytrace=False,
        )
    return result


# --- Part A: reading the map -----------------------------------------------------------


def check_part_a(value, expected, name):
    if value is None:
        pytest.fail(f"Part A: fill in {name} in task.py", pytrace=False)
    if not isinstance(value, tuple | list) or len(value) != 2:
        pytest.fail(f"Part A: {name} must be a pair (row, col), for example (2, 4)", pytrace=False)
    if tuple(value) != expected:
        pytest.fail(
            f"Part A: {name} is not right yet. Count rows from the top and columns from the "
            "left, both starting at 0, and give the row first.",
            pytrace=False,
        )


def test_part_a_start(impl):
    check_part_a(impl.START, SMALL.start, "START")


def test_part_a_dock(impl):
    check_part_a(impl.DOCK, SMALL.dock, "DOCK")


# --- Part B: free_neighbours -----------------------------------------------------------


@pytest.mark.parametrize(
    "cell, expected",
    [
        ((1, 1), [(1, 2), (2, 1)]),
        ((2, 3), [(1, 3), (2, 4), (3, 3)]),
        ((1, 5), [(2, 5)]),
        ((2, 5), [(1, 5), (3, 5), (2, 4)]),
    ],
)
def test_free_neighbours_in_order(impl, cell, expected):
    result = neighbours(impl, SMALL, cell)
    assert result == expected, (
        f"free_neighbours(small, {cell}) should list the free cells in the order N, E, S, W"
    )


def test_free_neighbours_skips_obstacles(impl):
    result = neighbours(impl, SMALL, (1, 2))
    assert (0, 2) not in result and (2, 2) not in result, (
        "a cell with '#' is an obstacle: it is never a free neighbour"
    )


def test_free_neighbours_never_leaves_the_map(impl):
    for cell, expected in [((0, 0), [(0, 1), (1, 0)]), ((2, 2), [(1, 2), (2, 1)])]:
        result = neighbours(impl, NO_BORDER, cell)
        assert result == expected, (
            f"on a map without border walls, free_neighbours({cell}) must not return cells "
            "outside the map (use warehouse.is_free, which also checks the edges)"
        )


def test_free_neighbours_returns_cells_not_directions(impl):
    result = neighbours(impl, SMALL, (1, 1))
    assert all(isinstance(c, tuple) and len(c) == 2 for c in result), (
        "return cells as (row, col) tuples, not direction names like 'E'"
    )


def test_task_does_not_import_reference(impl_path):
    found = find_reference_imports(impl_path)
    assert not found, f"task.py imports {found}: write free_neighbours yourself"
