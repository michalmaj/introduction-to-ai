import os

import nbformat
import pytest

from introai.authoring.notebooks import (
    NotebookFailed,
    find_notebooks,
    isolated_environment,
    main,
    run_notebook,
)


def make_notebook(path, *sources):
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(source) for source in sources]
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, path)
    return path


def test_find_notebooks_skips_checkpoints(tmp_path):
    a = make_notebook(tmp_path / "modules/02/01/experiments.ipynb", "x = 1")
    b = make_notebook(tmp_path / "modules/02/01/experiments.pl.ipynb", "x = 1")
    make_notebook(tmp_path / "modules/02/01/.ipynb_checkpoints/experiments.ipynb", "x = 1")
    make_notebook(tmp_path / "elsewhere/other.ipynb", "x = 1")
    assert find_notebooks(tmp_path) == [a, b]


def test_isolated_environment_sets_and_restores(tmp_path):
    before = dict(os.environ)
    with isolated_environment(tmp_path):
        assert os.environ["INTROAI_IMPLEMENTATION"] == "reference"
        assert os.environ["MPLBACKEND"] == "Agg"
        for name in (
            "MPLCONFIGDIR",
            "IPYTHONDIR",
            "JUPYTER_CONFIG_DIR",
            "JUPYTER_DATA_DIR",
            "JUPYTER_RUNTIME_DIR",
        ):
            assert os.environ[name].startswith(str(tmp_path))
    assert dict(os.environ) == before


def test_isolated_environment_can_select_mine(tmp_path):
    with isolated_environment(tmp_path, implementation="mine"):
        assert os.environ["INTROAI_IMPLEMENTATION"] == "mine"


def test_run_notebook_uses_isolated_headless_environment(tmp_path):
    path = make_notebook(
        tmp_path / "check.ipynb",
        'import os\nassert os.environ["INTROAI_IMPLEMENTATION"] == "reference"',
        'import matplotlib\nassert matplotlib.get_backend().lower() == "agg"',
        'import pathlib\nassert pathlib.Path.cwd().name == "' + tmp_path.name + '"',
    )
    original = path.read_bytes()
    run_notebook(path)
    assert path.read_bytes() == original


def test_run_notebook_reports_failing_cell(tmp_path):
    path = make_notebook(tmp_path / "bad.ipynb", "x = 1", "1 / 0")
    with pytest.raises(NotebookFailed) as info:
        run_notebook(path)
    assert info.value.cell_index == 1
    assert info.value.path == path


def test_main_runs_given_notebooks(tmp_path, capsys):
    good = make_notebook(tmp_path / "good.ipynb", "x = 1")
    bad = make_notebook(tmp_path / "bad.ipynb", "raise ValueError('boom')")
    assert main([str(good)]) == 0
    assert main([str(good), str(bad)]) == 1
    assert "bad.ipynb" in capsys.readouterr().out
