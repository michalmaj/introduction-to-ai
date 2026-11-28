import pytest

from introai.authoring.blocks import BlockError, process_file, render_block

WORKED_BARE = """\
```mermaid
graph TD
    A["▲ A"] --> B["▼ B"]
    A --> C["▼ C"]
    A --> D["▼ D"]
    B --> B1(["B1: 4"])
    B --> B2(["B2: 9"])
    B --> B3(["B3: 6"])
    C --> C1(["C1: 2"])
    C --> C2(["C2: 7"])
    C --> C3(["C3: 1"])
    D --> D1(["D1: 5"])
    D --> D2(["D2: 3"])
    D --> D3(["D3: 8"])
```"""

WORKED_MINIMAX = """\
```mermaid
graph TD
    A["▲ A = 4"] ==> B["▼ B = 4"]
    A --> C["▼ C = 1"]
    A --> D["▼ D = 3"]
    B ==> B1(["B1: 4"])
    B --> B2(["B2: 9"])
    B --> B3(["B3: 6"])
    C --> C1(["C1: 2"])
    C --> C2(["C2: 7"])
    C --> C3(["C3: 1"])
    D --> D1(["D1: 5"])
    D --> D2(["D2: 3"])
    D --> D3(["D3: 8"])
```"""

WORKED_ALPHA_BETA = """\
```mermaid
graph TD
    A["▲ A = 4"] ==> B["▼ B = 4"]
    A --> C["▼ C ≤ 2"]
    A --> D["▼ D ≤ 3"]
    B ==> B1(["B1: 4"])
    B --> B2(["B2: 9"])
    B --> B3(["B3: 6"])
    C --> C1(["C1: 2"])
    C --> C2(["C2: 7"])
    C --> C3(["C3: 1"])
    D --> D1(["D1: 5"])
    D --> D2(["D2: 3"])
    D --> D3(["D3: 8"])
    classDef pruned stroke-dasharray: 5 4
    class C2,C3,D3 pruned
```"""

EVALUATION_DEPTH_ONE = """\
```mermaid
graph TD
    A["▲ A = 6"] --> B["▼ B: e = 5"]
    A --> C["▼ C: e = 2"]
    A ==> D["▼ D: e = 6"]
```"""

WORKED_TABLE_PL = """\
| Krok | Węzeł | α | β | v | Co się stało |
|---|---|---|---|---|---|
| 1 | B1 | −∞ | +∞ | 4 | liść |
| 2 | B2 | −∞ | 4 | 9 | liść |
| 3 | B3 | −∞ | 4 | 6 | liść |
| 4 | ▼ B | −∞ | 4 | 4 | zwraca 4 |
| 5 | C1 | 4 | +∞ | 2 | liść |
| 6 | ▼ C | 4 | 2 | 2 | odcięcie: v ≤ α, pominięte C2, C3 |
| 7 | D1 | 4 | +∞ | 5 | liść |
| 8 | D2 | 4 | 5 | 3 | liść |
| 9 | ▼ D | 4 | 3 | 3 | odcięcie: v ≤ α, pominięte D3 |
| 10 | ▲ A | 4 | +∞ | 4 | zwraca 4 |

Wartość korzenia: **4**, ruch: **B**. Pominięte liście: C2, C3, D3."""


def test_bare_game_tree():
    assert render_block("game-tree", {"example": "worked_tree"}) == WORKED_BARE


def test_game_tree_with_minimax_values():
    params = {"example": "worked_tree", "values": "minimax"}
    assert render_block("game-tree", params) == WORKED_MINIMAX


def test_game_tree_with_alpha_beta_pruning():
    params = {"example": "worked_tree", "values": "alpha-beta"}
    assert render_block("game-tree", params) == WORKED_ALPHA_BETA


def test_alpha_beta_tree_marks_bounds_of_max_nodes_and_pruned_subtrees():
    params = {"example": "alpha_beta_exercise", "values": "alpha-beta"}
    text = render_block("game-tree", params)
    assert 'F["▲ F ≥ 7"]' in text
    assert 'H["▲ H ≤ 4"]' in text
    assert 'J["▲ J"]' in text
    assert "class N,J,U,V pruned" in text


def test_game_tree_cut_off_at_a_depth_shows_the_evaluations():
    params = {"example": "evaluation_tree", "values": "minimax", "depth": "1"}
    assert render_block("game-tree", params) == EVALUATION_DEPTH_ONE


def test_alpha_beta_table_in_polish():
    params = {"example": "worked_tree", "lang": "pl"}
    assert render_block("alpha-beta-table", params) == WORKED_TABLE_PL


def test_alpha_beta_table_in_english():
    text = render_block("alpha-beta-table", {"example": "worked_tree", "lang": "en"})
    assert text.startswith("| Step | Node | α | β | v | What happened |\n|---|---|---|---|---|---|")
    assert "| 4 | ▼ B | −∞ | 4 | 4 | returns 4 |" in text
    assert "| 6 | ▼ C | 4 | 2 | 2 | cutoff: v ≤ α, skipped C2, C3 |" in text
    assert text.endswith("Root value: **4**, move: **B**. Pruned leaves: C2, C3, D3.")


def test_alpha_beta_table_on_equal_values():
    text = render_block("alpha-beta-table", {"example": "ties_tree", "lang": "en"})
    assert "cutoff: v ≤ α, skipped C2" in text
    assert text.endswith("Pruned leaves: C2.")


@pytest.mark.parametrize(
    "kind, params, message",
    [
        ("game-tree", {"example": "nope"}, "unknown example 'nope'"),
        ("game-tree", {"example": "worked_tree", "values": "max"}, "unknown values 'max'"),
        ("game-tree", {"example": "worked_tree", "depth": "1"}, "depth"),
        (
            "game-tree",
            {"example": "evaluation_tree", "values": "minimax", "depth": "x"},
            "depth",
        ),
        ("game-tree", {"example": "worked_tree", "values": "minimax", "depth": "1"}, "evaluat"),
        ("alpha-beta-table", {"example": "worked_tree", "lang": "de"}, "unknown lang 'de'"),
        ("alpha-beta-table", {"example": "nope", "lang": "pl"}, "unknown example 'nope'"),
    ],
)
def test_bad_game_blocks(kind, params, message):
    with pytest.raises(BlockError, match=message):
        render_block(kind, params)


@pytest.mark.parametrize(
    "marker, refused",
    [
        ("<!-- generated:game-tree example=minimax_exercise values=minimax -->", True),
        ("<!-- generated:game-tree example=alpha_beta_exercise values=alpha-beta -->", True),
        ("<!-- generated:alpha-beta-table example=alpha_beta_exercise lang=pl -->", True),
        ("<!-- generated:game-tree example=minimax_exercise -->", False),
        ("<!-- generated:game-tree example=worked_tree values=minimax -->", False),
    ],
)
def test_game_blocks_that_reveal_part_a_are_refused_in_lessons_only(tmp_path, marker, refused):
    lesson = tmp_path / "modules/03/01/README.pl.md"
    answers = tmp_path / "solutions/03/01/answers.pl.md"
    for page in (lesson, answers):
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(marker + "\n<!-- /generated -->\n")
    problems = process_file(lesson, check=False, repo_root=tmp_path)
    assert any("would reveal Part A answers" in p for p in problems) == refused
    assert process_file(answers, check=False, repo_root=tmp_path) == []
