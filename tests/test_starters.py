"""Every starter that raises NotImplementedError must point to the notebook's reference switch."""

import ast
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
STARTERS = sorted((REPO / "modules").rglob("task.py"))


def not_implemented_messages(path: Path) -> list[str]:
    messages = []
    for node in ast.walk(ast.parse(path.read_bytes())):
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
            func = node.exc.func
            if isinstance(func, ast.Name) and func.id == "NotImplementedError":
                parts = [a.value for a in node.exc.args if isinstance(a, ast.Constant)]
                messages.append("".join(str(p) for p in parts))
    return messages


@pytest.mark.parametrize("starter", STARTERS, ids=lambda p: p.parent.name)
def test_starter_messages_point_to_the_reference_switch(starter):
    if not (starter.parent / "experiments.pl.ipynb").exists():
        pytest.skip("lesson without a notebook")
    messages = not_implemented_messages(starter)
    assert messages, "a starter should raise NotImplementedError where the student works"
    for message in messages:
        assert "TODO" in message and 'IMPLEMENTATION = "reference"' in message
