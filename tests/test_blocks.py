from pathlib import Path

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


REFLEX_PL = """\
| Krok | Pole robota | Percepcja: paczka; wolne kierunki | Akcja | Punkty po kroku |
|---|---|---|---|---|
| 1 | (1, 1) | nie; E, S | E | -1 |
| 2 | (1, 2) | nie; E, W | E | -2 |
| 3 | (1, 3) | tak; S, W | PICK | 7 |
| 4 | (1, 3) | nie; S, W | S | 6 |
| 5 | (2, 3) | nie; N, E, S | N | 5 |
| 6 | (1, 3) | nie; S, W | S | 4 |

Po 6 krokach: zebrane paczki 1, wynik 4."""


def test_episode_table_reflex_agent(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    params = {"agent": "reflex", "map": "parcels", "steps": "6", "lang": "pl"}
    assert render_block("episode-table", params, repo_root=repo) == REFLEX_PL
    english = render_block("episode-table", {**params, "lang": "en"}, repo_root=repo)
    assert english.splitlines()[0] == (
        "| Step | Robot's cell | Percept: parcel; free directions | Action | Score after the step |"
    )
    assert "| 3 | (1, 3) | yes; S, W | PICK | 7 |" in english
    assert english.endswith("After 6 steps: parcels collected 1, score 4.")


def test_graph_block_shows_weights():
    text = render_block("graph", {"example": "weighted_example"})
    assert "    A ---|2| B" in text and "    S ---|6| B" not in text and "    B ---|6| S" in text


UCS_PL = """\
| Krok | Zdjęty | g | f | Wynik | Frontier: stan f, w kolejności zdejmowania | Najlepsze znane g |
|---|---|---|---|---|---|---|
| 1 | S | 0 | 0 | rozwinięty | A 1, B 6 | A 1, B 6, S 0 |
| 2 | A | 1 | 1 | rozwinięty | B 3, B 6, D 8 | A 1, B 3, D 8, S 0 |
| 3 | B | 3 | 3 | rozwinięty | C 5, B 6, D 8, G 9 | A 1, B 3, C 5, D 8, G 9, S 0 |
| 4 | C | 5 | 5 | rozwinięty | B 6, G 7, D 8, G 9 | A 1, B 3, C 5, D 8, G 7, S 0 |
| 5 | B | 6 | 6 | pominięty | G 7, D 8, G 9 | A 1, B 3, C 5, D 8, G 7, S 0 |
| 6 | G | 7 | 7 | cel | D 8, G 9 | A 1, B 3, C 5, D 8, G 7, S 0 |

Cel **G** osiągnięty kosztem 7. Ścieżka: S → A → B → C → G."""


def test_ucs_trace_table():
    params = {"algorithm": "ucs", "example": "weighted_example", "lang": "pl"}
    assert render_block("trace-table", params) == UCS_PL
    english = render_block("trace-table", {**params, "lang": "en"})
    assert english.splitlines()[0] == (
        "| Step | Popped | g | f | Outcome | Frontier: state f, in removal order | Best known g |"
    )
    assert english.endswith("Goal **G** reached at cost 7. Path: S → A → B → C → G.")


def test_a_star_and_greedy_trace_tables():
    astar = render_block(
        "trace-table", {"algorithm": "astar", "example": "weighted_example", "lang": "en"}
    )
    assert "| 1 | S | 0 | 5 | expanded | A 6, B 9 |" in astar
    greedy = render_block(
        "trace-table", {"algorithm": "greedy", "example": "weighted_example", "lang": "en"}
    )
    assert greedy.endswith("Goal **G** reached at cost 12. Path: S → B → G.")


TREE_PL = """\
| Głębokość | Węzły (ich stany) | Liczba węzłów | Różne stany |
|---|---|---|---|
| 0 | S | 1 | 1 |
| 1 | A, B | 2 | 2 |
| 2 | C, S, C, D, S | 5 | 3 |"""


def test_tree_levels_block():
    params = {"example": "worked_example", "depth": "2", "lang": "pl"}
    assert render_block("tree-levels", params) == TREE_PL
    english = render_block("tree-levels", {**params, "lang": "en"})
    assert english.splitlines()[0] == "| Depth | Nodes (their states) | Nodes | Distinct states |"


def test_tree_levels_of_an_exercise_are_rejected_in_lessons(tmp_path):
    lesson = tmp_path / "modules/02/01/README.md"
    lesson.parent.mkdir(parents=True)
    block = "<!-- generated:tree-levels example=exercise depth=2 lang=en -->"
    lesson.write_text(f"{block}\n<!-- /generated -->\n")
    problems = process_file(lesson, check=False, repo_root=tmp_path)
    assert any("would reveal Part A answers" in p for p in problems)


TREE_DIAGRAM = """\
```mermaid
graph TD
    n0[S] --> n1[A]
    n0[S] --> n2[B]
    n1[A] --> n3[C]
    n1[A] --> n4[S]
    n2[B] --> n5[C]
    n2[B] --> n6[D]
    n2[B] --> n7[S]
    classDef repeated stroke-dasharray: 5 4
    class n4,n5,n7 repeated
```"""


def test_search_tree_block_dashes_repeated_states():
    assert render_block("search-tree", {"example": "worked_example", "depth": "2"}) == TREE_DIAGRAM


def test_tree_blocks_need_a_whole_depth():
    for kind in ("search-tree", "tree-levels"):
        try:
            render_block(kind, {"example": "worked_example", "depth": "two", "lang": "en"})
        except ValueError as error:
            assert "depth" in str(error)
        else:
            raise AssertionError(f"{kind} accepted a depth that is not a number")


def test_heuristic_block_lists_h_for_every_state():
    table = render_block("heuristic", {"example": "weighted_example", "lang": "pl"})
    assert (
        table == "| Stan | A | B | C | D | G | S |\n|---|---|---|---|---|---|---|\n"
        "| h | 5 | 3 | 2 | 1 | 0 | 5 |"
    )
    english = render_block("heuristic", {"example": "weighted_example", "lang": "en"})
    assert english.startswith("| State | A |")


def test_heuristic_of_an_exercise_is_allowed_in_lessons(tmp_path):
    lesson = tmp_path / "modules/02/04/README.md"
    lesson.parent.mkdir(parents=True)
    lesson.write_text(
        "<!-- generated:heuristic example=astar_exercise lang=en -->\n<!-- /generated -->\n"
    )
    assert process_file(lesson, check=False, repo_root=tmp_path) == []
    assert "| h | 7 | 6 | 8 | 4 | 9 | 2 | 0 |" in lesson.read_text()
