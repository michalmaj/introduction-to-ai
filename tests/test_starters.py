"""Every starter with code to write must point to the notebook's reference switch."""

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


def defines_code(path: Path) -> bool:
    """Whether a starter has functions or classes to implement (a Part-A-only one has none)."""
    tree = ast.parse(path.read_bytes())
    return any(isinstance(node, ast.FunctionDef | ast.ClassDef) for node in tree.body)


@pytest.mark.parametrize("starter", STARTERS, ids=lambda p: p.parent.name)
def test_starter_messages_point_to_the_reference_switch(starter):
    if not (starter.parent / "experiments.pl.ipynb").exists():
        pytest.skip("lesson without a notebook")
    if not defines_code(starter):
        pytest.skip("Part A only: nothing to implement")
    messages = not_implemented_messages(starter)
    assert messages, "a starter should raise NotImplementedError where the student works"
    for message in messages:
        assert "TODO" in message and 'IMPLEMENTATION = "reference"' in message


def test_only_starters_with_code_must_raise_not_implemented(tmp_path):
    constants = tmp_path / "part_a_only.py"
    constants.write_text("ANSWERS: dict | None = None\n")
    code = tmp_path / "with_function.py"
    code.write_text("def solve():\n    return 1\n")
    assert not defines_code(constants)
    assert defines_code(code) and not_implemented_messages(code) == []
