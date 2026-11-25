"""Keep the English notebook in step with its Polish source.

Polish is the source language (D-011): edit ``X.pl.ipynb``, then run::

    uv run python tools/sync_notebooks.py

For every pair the tool copies the code cells (and cell ids) from the Polish
notebook into the English one, keeps the English Markdown as it is, and clears
outputs in both files. Both notebooks must already have the same cell
structure (the same sequence of Markdown and code cells); if they do not, the
English file is left untouched and the difference is reported, because new
Markdown cells need a human translation.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

import nbformat


def _clear_outputs(notebook: nbformat.NotebookNode) -> None:
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None


def sync_pair(source: Path, target: Path) -> list[str]:
    """Copy code cells from ``source`` (Polish) to ``target`` (English); return problems."""
    polish = nbformat.read(source, as_version=4)
    english = nbformat.read(target, as_version=4)
    polish_types = [cell.cell_type for cell in polish.cells]
    english_types = [cell.cell_type for cell in english.cells]
    if polish_types != english_types:
        first = next(
            (i for i, (a, b) in enumerate(zip(polish_types, english_types), start=1) if a != b),
            min(len(polish_types), len(english_types)) + 1,
        )
        return [
            f"{target.name}: cell structure differs from {source.name} (first difference at "
            f"cell {first}); add or remove the matching Markdown cells by hand"
        ]

    for polish_cell, english_cell in zip(polish.cells, english.cells):
        english_cell.id = polish_cell.id
        if polish_cell.cell_type == "code":
            english_cell.source = polish_cell.source
    for notebook, path in ((polish, source), (english, target)):
        _clear_outputs(notebook)
        nbformat.write(notebook, path)
    return []


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Copy notebook code from Polish to English.")
    parser.add_argument("notebooks", nargs="*", type=Path, help="Polish notebooks (default: all)")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    modules = args.repo_root / "modules"
    sources = args.notebooks or (sorted(modules.rglob("*.pl.ipynb")) if modules.is_dir() else [])
    problems: list[str] = []
    for source in sources:
        if ".ipynb_checkpoints" in source.parts:
            continue
        target = source.with_name(source.name.replace(".pl.ipynb", ".ipynb"))
        if not target.exists():
            problems.append(f"{source}: missing English pair {target.name}")
            continue
        problems += sync_pair(source, target)
    for problem in problems:
        print(problem)
    print(f"notebook sync: {len(sources)} pair(s), {len(problems)} problem(s)")
    return 1 if problems else 0
