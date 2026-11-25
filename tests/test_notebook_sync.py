import nbformat

from introai.authoring.notebook_sync import main, sync_pair


def write(path, cells, outputs=False):
    nb = nbformat.v4.new_notebook()
    for kind, source, cell_id in cells:
        cell = (
            nbformat.v4.new_markdown_cell(source)
            if kind == "md"
            else nbformat.v4.new_code_cell(source)
        )
        cell.id = cell_id
        if outputs and kind == "code":
            cell.outputs = [nbformat.v4.new_output("stream", text="hi")]
            cell.execution_count = 1
        nb.cells.append(cell)
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, path)


def cells(path):
    return [(c.cell_type, c.source, c.id) for c in nbformat.read(path, as_version=4).cells]


def test_sync_copies_code_and_keeps_translated_markdown(tmp_path):
    pl, en = tmp_path / "e.pl.ipynb", tmp_path / "e.ipynb"
    write(pl, [("md", "Wstęp", "md-intro"), ("code", "x = 2", "code-a")], outputs=True)
    write(en, [("md", "Intro", "md-1"), ("code", "x = 1", "code-1")])
    assert sync_pair(pl, en) == []
    assert cells(en) == [("markdown", "Intro", "md-intro"), ("code", "x = 2", "code-a")]
    for path in (pl, en):
        nb = nbformat.read(path, as_version=4)
        code = [c for c in nb.cells if c.cell_type == "code"]
        assert all(c.outputs == [] and c.execution_count is None for c in code)


def test_sync_refuses_different_structure(tmp_path):
    pl, en = tmp_path / "e.pl.ipynb", tmp_path / "e.ipynb"
    write(pl, [("md", "Wstęp", "a"), ("code", "x = 2", "b"), ("md", "Koniec", "c")])
    write(en, [("md", "Intro", "a"), ("code", "x = 1", "b")])
    before = en.read_bytes()
    problems = sync_pair(pl, en)
    assert any("cell structure differs" in p for p in problems)
    assert en.read_bytes() == before


def test_main_syncs_all_pairs(tmp_path, capsys):
    pl = tmp_path / "modules/a/b/e.pl.ipynb"
    en = tmp_path / "modules/a/b/e.ipynb"
    write(pl, [("code", "y = 3", "c")])
    write(en, [("code", "y = 0", "c")])
    assert main(["--repo-root", str(tmp_path)]) == 0
    assert cells(en) == [("code", "y = 3", "c")]
