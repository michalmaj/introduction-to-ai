from pathlib import Path

import pytest

from introai.search.examples import exercise
from introai.testing.impl import load_module

STARTER = Path(__file__).resolve().parents[1] / "modules/02_search/02_bfs_dfs/task.py"


@pytest.mark.parametrize("name", ["bfs", "dfs"])
def test_starter_points_to_the_reference_switch(name):
    starter = load_module(STARTER)
    with pytest.raises(NotImplementedError, match='IMPLEMENTATION = "reference"'):
        getattr(starter, name)(exercise())


def test_starter_part_a_is_empty():
    starter = load_module(STARTER)
    for name in ("BFS_EXPANSION_ORDER", "BFS_PATH", "DFS_EXPANSION_ORDER", "DFS_PATH"):
        assert getattr(starter, name) is None
