"""Static checks on a student's source file."""

from __future__ import annotations

import ast
from pathlib import Path


def _is_reference(dotted: str) -> bool:
    parts = dotted.split(".")
    return len(parts) >= 3 and parts[0] == "introai" and parts[2] == "reference"


def find_reference_imports(path: Path) -> list[str]:
    """Dotted names imported from any ``introai.<area>.reference`` module.

    Lessons ask you to write an algorithm yourself, so ``task.py`` must not
    import the course's reference version of it.
    """
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [alias.name for alias in node.names if _is_reference(alias.name)]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            if _is_reference(node.module):
                found += [f"{node.module}.{alias.name}" for alias in node.names]
            else:
                found += [
                    f"{node.module}.{alias.name}"
                    for alias in node.names
                    if _is_reference(f"{node.module}.{alias.name}")
                ]
    return found
