"""Repository content checks: bilingual pairs, links and clean notebooks.

Rules (decision D-011):

- every Markdown file ``X.md`` (English) has a Polish pair ``X.pl.md`` and vice
  versa, except files in ``UNPAIRED_ALLOWED``;
- the first non-empty line is the language switch,
  ``**English** | [Polski](X.pl.md)`` or ``[English](X.md) | **Polski**``;
- both files of a pair have the same sequence of heading levels;
- relative links point to existing files;
- notebooks come in pairs ``X.ipynb`` / ``X.pl.ipynb`` with identical code cells
  and are committed without outputs.

Hidden directories (``.git``, ``.github``, ``.venv`` ...), ``decisions/`` and
``__pycache__`` are not checked.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections.abc import Iterator, Sequence
from pathlib import Path
from urllib.parse import unquote

UNPAIRED_ALLOWED = frozenset({"LICENSE-CONTENT.md"})
_SKIPPED_DIRS = {"decisions", "__pycache__"}
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_INLINE_CODE = re.compile(r"`[^`]*`")
_FENCE = re.compile(r"^\s*(```|~~~)")


def _files(repo_root: Path, suffix: str) -> Iterator[Path]:
    for directory, subdirs, files in os.walk(repo_root):
        subdirs[:] = sorted(d for d in subdirs if not d.startswith(".") and d not in _SKIPPED_DIRS)
        for name in sorted(files):
            if name.endswith(suffix):
                yield Path(directory) / name


def _pair(path: Path, suffix: str) -> tuple[Path, bool]:
    """Return the path of the other language version and whether ``path`` is Polish."""
    name = path.name
    polish_suffix = ".pl" + suffix
    if name.endswith(polish_suffix):
        return path.with_name(name[: -len(polish_suffix)] + suffix), True
    return path.with_name(name[: -len(suffix)] + polish_suffix), False


def _lines_outside_fences(text: str) -> Iterator[str]:
    in_fence = False
    for line in text.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line


def _heading_levels(text: str) -> list[int]:
    levels = []
    for line in _lines_outside_fences(text):
        match = re.match(r"^(#{1,6})\s", line)
        if match:
            levels.append(len(match.group(1)))
    return levels


def _first_nonempty_line(text: str) -> str:
    return next((line.strip() for line in text.splitlines() if line.strip()), "")


def _check_markdown(path: Path, repo_root: Path) -> list[str]:
    rel = path.relative_to(repo_root).as_posix()
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    if path.name not in UNPAIRED_ALLOWED:
        pair, is_polish = _pair(path, ".md")
        if not pair.exists():
            language = "English" if is_polish else "Polish"
            problems.append(f"{rel}: missing {language} pair {pair.name}")
        else:
            expected = (
                f"[English]({pair.name}) | **Polski**"
                if is_polish
                else f"**English** | [Polski]({pair.name})"
            )
            if _first_nonempty_line(text) != expected:
                problems.append(f"{rel}: first line must be '{expected}'")
            if not is_polish:
                mine = _heading_levels(text)
                theirs = _heading_levels(pair.read_text(encoding="utf-8"))
                if mine != theirs:
                    problems.append(
                        f"{rel}: heading structure differs from {pair.name} "
                        f"(levels {mine} vs {theirs})"
                    )

    for line in _lines_outside_fences(text):
        for target in _LINK.findall(_INLINE_CODE.sub("", line)):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_part = unquote(target.split("#", 1)[0])
            if file_part and not (path.parent / file_part).exists():
                problems.append(f"{rel}: broken link '{target}'")
    return problems


def _cells(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")).get("cells", [])


def _code_cells(path: Path) -> list[dict]:
    return [cell for cell in _cells(path) if cell.get("cell_type") == "code"]


def _first_difference(mine: list, theirs: list) -> int:
    """1-based index of the first differing element (or the first extra one)."""
    return next(
        (i for i, (a, b) in enumerate(zip(mine, theirs), start=1) if a != b),
        min(len(mine), len(theirs)) + 1,
    )


def _source(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def _check_notebook(path: Path, repo_root: Path) -> list[str]:
    rel = path.relative_to(repo_root).as_posix()
    problems: list[str] = []
    cells = _code_cells(path)
    for index, cell in enumerate(cells, start=1):
        if cell.get("outputs") or cell.get("execution_count") is not None:
            problems.append(
                f"{rel}: code cell {index} has outputs or an execution count; "
                "clear outputs before committing"
            )

    pair, is_polish = _pair(path, ".ipynb")
    if not pair.exists():
        language = "English" if is_polish else "Polish"
        problems.append(f"{rel}: missing {language} pair {pair.name}")
    elif not is_polish:
        my_types = [cell.get("cell_type") for cell in _cells(path)]
        their_types = [cell.get("cell_type") for cell in _cells(pair)]
        mine = [_source(cell) for cell in cells]
        theirs = [_source(cell) for cell in _code_cells(pair)]
        if my_types != their_types:
            first = _first_difference(my_types, their_types)
            problems.append(
                f"{rel}: cell structure differs from {pair.name} (first difference at cell {first})"
            )
        elif mine != theirs:
            first = _first_difference(mine, theirs)
            problems.append(
                f"{rel}: code cells differ from {pair.name} (first difference at code cell {first})"
            )
    return problems


def check_repository(repo_root: Path) -> list[str]:
    """Return every content problem in the repository (empty list when clean)."""
    repo_root = Path(repo_root)
    problems: list[str] = []
    for path in _files(repo_root, ".md"):
        problems += _check_markdown(path, repo_root)
    for path in _files(repo_root, ".ipynb"):
        problems += _check_notebook(path, repo_root)
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check bilingual content and notebooks.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    problems = check_repository(args.repo_root)
    for problem in problems:
        print(problem)
    print(f"content check: {len(problems)} problem(s)")
    return 1 if problems else 0
