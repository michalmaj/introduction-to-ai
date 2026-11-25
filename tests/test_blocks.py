from introai.authoring.blocks import main, process_file, render_block

BFS_PL = """\
| Krok | Rozwijany węzeł | Frontier (w kolejności zdejmowania) | Zbiór osiągniętych (reached) |
|---|---|---|---|
| 1 | S | A, B | A, B, S |
| 2 | A | B, C | A, B, C, S |
| 3 | B | C, D | A, B, C, D, S |
| 4 | C | D | A, B, C, D, S |

Cel **G** znaleziony podczas rozwijania **C**. Ścieżka: S → A → C → G."""

BFS_EN = """\
| Step | Expanded node | Frontier (in removal order) | Reached set |
|---|---|---|---|
| 1 | S | A, B | A, B, S |
| 2 | A | B, C | A, B, C, S |
| 3 | B | C, D | A, B, C, D, S |
| 4 | C | D | A, B, C, D, S |

Goal **G** found while expanding **C**. Path: S → A → C → G."""

DFS_PL = """\
| Krok | Zdjęty węzeł | Wynik | Frontier (w kolejności zdejmowania) | Rozwinięte |
|---|---|---|---|---|
| 1 | S | rozwinięty | A, B | S |
| 2 | A | rozwinięty | C, B | A, S |
| 3 | C | rozwinięty | B, G, B | A, C, S |
| 4 | B | rozwinięty | D, G, B | A, B, C, S |
| 5 | D | rozwinięty | G, G, B | A, B, C, D, S |
| 6 | G | cel | G, B | A, B, C, D, S |

Ścieżka: S → A → C → B → D → G."""

DFS_EN = """\
| Step | Popped node | Outcome | Frontier (in removal order) | Expanded |
|---|---|---|---|---|
| 1 | S | expanded | A, B | S |
| 2 | A | expanded | C, B | A, S |
| 3 | C | expanded | B, G, B | A, C, S |
| 4 | B | expanded | D, G, B | A, B, C, S |
| 5 | D | expanded | G, G, B | A, B, C, D, S |
| 6 | G | goal | G, B | A, B, C, D, S |

Path: S → A → C → B → D → G."""


def test_trace_tables_worked_example():
    params = {"example": "worked_example"}
    assert render_block("trace-table", {"algorithm": "bfs", "lang": "pl", **params}) == BFS_PL
    assert render_block("trace-table", {"algorithm": "bfs", "lang": "en", **params}) == BFS_EN
    assert render_block("trace-table", {"algorithm": "dfs", "lang": "pl", **params}) == DFS_PL
    assert render_block("trace-table", {"algorithm": "dfs", "lang": "en", **params}) == DFS_EN


def test_dfs_table_shows_skipped_pops():
    table = render_block("trace-table", {"algorithm": "dfs", "example": "cyclic", "lang": "en"})
    assert "| skipped |" in table
    assert table.endswith("The frontier is empty: the goal cannot be reached.")


def test_graph_block():
    assert render_block("graph", {"example": "disconnected"}) == (
        "```mermaid\ngraph LR\n    A --- B\n    C --- D\n```"
    )
    assert render_block("graph", {"example": "binary_tree"}).splitlines()[2] == "    R --> A"


def stale_page(root, relative):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Lesson\n\n"
        "<!-- generated:graph example=disconnected -->\n"
        "old content\n"
        "<!-- /generated -->\n\n"
        "Text after.\n"
    )
    return path


def test_round_trip(tmp_path):
    page = stale_page(tmp_path, "modules/02/01/README.md")
    before = page.read_text()
    problems = process_file(page, check=True, repo_root=tmp_path)
    assert any("out of date" in p for p in problems)
    assert page.read_text() == before
    assert process_file(page, check=False, repo_root=tmp_path) == []
    text = page.read_text()
    assert "    A --- B" in text and text.endswith("Text after.\n")
    assert process_file(page, check=True, repo_root=tmp_path) == []


def test_exercise_trace_is_rejected_in_lessons_only(tmp_path):
    marker = "<!-- generated:trace-table algorithm=bfs example=exercise lang=pl -->\n"
    lesson = tmp_path / "modules/02/01/README.pl.md"
    answers = tmp_path / "solutions/02/01/answers.pl.md"
    for page in (lesson, answers):
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(marker + "<!-- /generated -->\n")
    assert any(
        "would reveal Part A answers" in p
        for p in process_file(lesson, check=False, repo_root=tmp_path)
    )
    assert process_file(answers, check=False, repo_root=tmp_path) == []


def test_bad_blocks_are_reported(tmp_path):
    page = tmp_path / "modules/a/README.md"
    page.parent.mkdir(parents=True)
    page.write_text("<!-- generated:chart example=x -->\n<!-- /generated -->\n")
    assert any(
        "unknown generated block kind 'chart'" in p
        for p in process_file(page, check=True, repo_root=tmp_path)
    )
    page.write_text("<!-- generated:graph example=nope -->\n<!-- /generated -->\n")
    assert any(
        "unknown example 'nope'" in p for p in process_file(page, check=True, repo_root=tmp_path)
    )
    page.write_text("<!-- generated:graph example=cyclic -->\nno end\n")
    assert any("not closed" in p for p in process_file(page, check=True, repo_root=tmp_path))


def test_main_check_mode(tmp_path, capsys):
    stale_page(tmp_path, "modules/02/01/README.md")
    assert main(["--check", "--repo-root", str(tmp_path)]) == 1
    assert main(["--repo-root", str(tmp_path)]) == 0
    assert main(["--check", "--repo-root", str(tmp_path)]) == 0
