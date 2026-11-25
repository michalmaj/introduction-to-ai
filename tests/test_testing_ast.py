import pytest

from introai.testing.ast_checks import find_reference_imports


@pytest.mark.parametrize(
    "source, expected",
    [
        ("import introai.search.reference\n", ["introai.search.reference"]),
        ("import introai.search.reference as r\n", ["introai.search.reference"]),
        ("from introai.search.reference import bfs\n", ["introai.search.reference.bfs"]),
        ("from introai.search import reference\n", ["introai.search.reference"]),
        (
            "def f():\n    from introai.search.reference import dfs\n",
            ["introai.search.reference.dfs"],
        ),
        ("from introai.search import Node, expand\n", []),
        ("import introai.search\n", []),
        ("from introai import search\n", []),
        ("import reference\n", []),
    ],
)
def test_find_reference_imports(tmp_path, source, expected):
    path = tmp_path / "task.py"
    path.write_text(source)
    assert find_reference_imports(path) == expected


def test_find_reference_imports_tolerates_bom(tmp_path):
    path = tmp_path / "task.py"
    path.write_bytes("﻿from introai.search.reference import bfs\n".encode())
    assert find_reference_imports(path) == ["introai.search.reference.bfs"]
