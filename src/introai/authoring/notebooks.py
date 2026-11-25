"""Executing lesson notebooks headlessly, in an isolated environment.

Notebooks run with matplotlib's ``Agg`` backend (no windows) and with
temporary Jupyter, IPython and matplotlib directories, so checks never touch
the user's own configuration. ``INTROAI_IMPLEMENTATION`` tells the notebooks
whether to use the student's ``task.py`` ("mine") or the reference code.
Notebooks are never written back: committed notebooks stay without outputs.
"""

from __future__ import annotations

import argparse
import os
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

_ISOLATED_DIRS = (
    "MPLCONFIGDIR",
    "IPYTHONDIR",
    "JUPYTER_CONFIG_DIR",
    "JUPYTER_DATA_DIR",
    "JUPYTER_RUNTIME_DIR",
)


class NotebookFailed(Exception):
    """A notebook cell raised an error."""

    def __init__(self, path: Path, cell_index: int, message: str) -> None:
        super().__init__(f"{path}: cell {cell_index} failed: {message}")
        self.path = path
        self.cell_index = cell_index


def find_notebooks(repo_root: Path) -> list[Path]:
    """All lesson notebooks under ``modules/``, sorted."""
    modules = Path(repo_root) / "modules"
    if not modules.is_dir():
        return []
    return sorted(p for p in modules.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)


@contextmanager
def isolated_environment(base_dir: Path, implementation: str = "reference") -> Iterator[None]:
    """Temporarily set a headless, isolated environment; restore ``os.environ`` afterwards."""
    saved = dict(os.environ)
    try:
        os.environ["MPLBACKEND"] = "Agg"
        os.environ["INTROAI_IMPLEMENTATION"] = implementation
        for name in _ISOLATED_DIRS:
            directory = Path(base_dir) / name.lower()
            directory.mkdir(parents=True, exist_ok=True)
            os.environ[name] = str(directory)
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


def run_notebook(path: Path, timeout: int = 300, implementation: str = "reference") -> None:
    """Execute every cell of ``path``; raise :class:`NotebookFailed` on the first error."""
    path = Path(path)
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    with tempfile.TemporaryDirectory(prefix="introai-nb-") as tmp:
        with isolated_environment(Path(tmp), implementation):
            try:
                client.execute()
            except CellExecutionError as error:
                for index, cell in enumerate(notebook.cells):
                    if any(o.get("output_type") == "error" for o in cell.get("outputs", [])):
                        raise NotebookFailed(path, index, str(error).splitlines()[-1]) from error
                raise NotebookFailed(path, -1, str(error)) from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute lesson notebooks headlessly.")
    parser.add_argument("notebooks", nargs="*", type=Path, help="notebooks (default: all)")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--implementation", choices=("reference", "mine"), default="reference")
    args = parser.parse_args(argv)

    notebooks = args.notebooks or find_notebooks(args.repo_root)
    failures = 0
    for notebook in notebooks:
        try:
            run_notebook(notebook, implementation=args.implementation)
            print(f"ok      {notebook}")
        except NotebookFailed as failure:
            failures += 1
            print(f"FAILED  {failure}")
    print(f"notebooks: {len(notebooks)} run, {failures} failed")
    return 1 if failures else 0
