import nbformat

from introai.authoring.content import check_repository, main

EN_SWITCH = "**English** | [Polski]({}.pl.md)\n\n"
PL_SWITCH = "[English]({}.md) | **Polski**\n\n"


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def write_pair(root, stem, en_body="# Title\n\n## Part\n", pl_body="# Tytuł\n\n## Część\n"):
    name = stem.split("/")[-1]
    write(root, f"{stem}.md", EN_SWITCH.format(name) + en_body)
    write(root, f"{stem}.pl.md", PL_SWITCH.format(name) + pl_body)


def write_notebook(root, relative, code_cells, outputs=False):
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_markdown_cell("text")]
    for source in code_cells:
        cell = nbformat.v4.new_code_cell(source)
        if outputs:
            cell.outputs = [nbformat.v4.new_output("stream", text="hi")]
            cell.execution_count = 1
        nb.cells.append(cell)
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, path)


def test_clean_tree_has_no_problems(tmp_path):
    write_pair(tmp_path, "README", en_body="# T\n\nSee [map](docs/MAP.md#top).\n")
    write_pair(tmp_path, "docs/MAP")
    write(
        tmp_path,
        "README.pl.md",
        PL_SWITCH.format("README") + "# T\n\nZob. [mapa](docs/MAP.pl.md).\n",
    )
    write(tmp_path, "LICENSE-CONTENT.md", "License text\n")
    write_notebook(tmp_path, "modules/a/experiments.ipynb", ["x = 1"])
    write_notebook(tmp_path, "modules/a/experiments.pl.ipynb", ["x = 1"])
    assert check_repository(tmp_path) == []


def test_missing_polish_pair(tmp_path):
    write(tmp_path, "README.md", EN_SWITCH.format("README") + "# T\n")
    assert any("README.md" in p and "missing Polish pair" in p for p in check_repository(tmp_path))


def test_missing_english_pair(tmp_path):
    write(tmp_path, "README.pl.md", PL_SWITCH.format("README") + "# T\n")
    problems = check_repository(tmp_path)
    assert any("README.pl.md" in p and "missing English pair" in p for p in problems)


def test_wrong_language_switch(tmp_path):
    write_pair(tmp_path, "README")
    write(tmp_path, "README.md", "# Title\n\n## Part\n")
    problems = check_repository(tmp_path)
    assert any("README.md" in p and "first line must be" in p for p in problems)


def test_heading_structure_mismatch(tmp_path):
    write_pair(tmp_path, "README", en_body="# T\n\n## A\n\n## B\n", pl_body="# T\n\n## A\n")
    assert any("heading structure differs" in p for p in check_repository(tmp_path))


def test_headings_inside_code_fences_are_ignored(tmp_path):
    write_pair(tmp_path, "README", en_body="# T\n\n```\n# comment\n```\n", pl_body="# T\n")
    assert check_repository(tmp_path) == []


def test_broken_link(tmp_path):
    write_pair(tmp_path, "README", en_body="# T\n\nSee [x](nope.md).\n", pl_body="# T\n")
    assert any("broken link 'nope.md'" in p for p in check_repository(tmp_path))


def test_external_anchor_and_fenced_links_are_ignored(tmp_path):
    body = "# T\n\n[a](https://example.com) [b](#top) [c](mailto:x@y.z)\n\n```\n[d](nope.md)\n```\n"
    write_pair(tmp_path, "README", en_body=body, pl_body="# T\n")
    assert check_repository(tmp_path) == []


def test_unpaired_license_is_allowed(tmp_path):
    write(tmp_path, "LICENSE-CONTENT.md", "License\n")
    assert check_repository(tmp_path) == []


def test_private_and_hidden_directories_are_skipped(tmp_path):
    write(tmp_path, "decisions/notes.md", "private\n")
    write(tmp_path, ".superpowers/sdd/progress.md", "ledger\n")
    write(tmp_path, ".github/PULL_REQUEST_TEMPLATE.md", "template\n")
    assert check_repository(tmp_path) == []


def test_notebook_missing_pair(tmp_path):
    write_notebook(tmp_path, "modules/a/experiments.ipynb", ["x = 1"])
    assert any("missing Polish pair" in p for p in check_repository(tmp_path))


def test_notebook_code_cells_must_match(tmp_path):
    write_notebook(tmp_path, "modules/a/experiments.ipynb", ["x = 1", "y = 2"])
    write_notebook(tmp_path, "modules/a/experiments.pl.ipynb", ["x = 1", "y = 3"])
    problems = check_repository(tmp_path)
    assert any("code cells differ" in p and "code cell 2" in p for p in problems)


def test_notebook_outputs_must_be_cleared(tmp_path):
    write_notebook(tmp_path, "modules/a/experiments.ipynb", ["x = 1"], outputs=True)
    write_notebook(tmp_path, "modules/a/experiments.pl.ipynb", ["x = 1"])
    problems = check_repository(tmp_path)
    assert any("experiments.ipynb" in p and "clear outputs" in p for p in problems)


def test_main_exit_codes(tmp_path, capsys):
    assert main(["--repo-root", str(tmp_path)]) == 0
    write(tmp_path, "README.md", "# T\n")
    assert main(["--repo-root", str(tmp_path)]) == 1
    assert "missing Polish pair" in capsys.readouterr().out


def write_cells(root, relative, cells):
    """cells: list of ("md" | "code", source)."""
    nb = nbformat.v4.new_notebook()
    nb.cells = [
        nbformat.v4.new_markdown_cell(s) if kind == "md" else nbformat.v4.new_code_cell(s)
        for kind, s in cells
    ]
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, path)


def test_notebook_cell_structure_must_match(tmp_path):
    write_cells(tmp_path, "modules/a/e.ipynb", [("md", "Intro"), ("code", "x = 1"), ("md", "Bye")])
    write_cells(tmp_path, "modules/a/e.pl.ipynb", [("md", "Wstęp"), ("code", "x = 1")])
    problems = check_repository(tmp_path)
    assert any("cell structure differs" in p and "cell 3" in p for p in problems)
