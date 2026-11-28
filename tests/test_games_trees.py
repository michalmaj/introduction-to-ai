import pytest

from introai.games import examples
from introai.games.examples import GAME_EXAMPLES, GAME_EXERCISES, tree_evaluation
from introai.games.trees import GameTree
from introai.trace import record


def small():
    return GameTree({"A": ["B", "C"], "B": ["D", "E"]}, {"C": 1, "D": 2, "E": 3}, "A")


def shape(tree, node=None):
    """The tree as nested (name, value) and (name, [children]) pairs."""
    node = tree.initial if node is None else node
    if tree.is_terminal(node):
        return (node, tree.leaves[node])
    return (node, [shape(tree, child) for child in tree.actions(node)])


def test_players_alternate_with_depth():
    tree = small()
    assert tree.players == ("MAX", "MIN")
    assert [tree.to_move(node) for node in "ABCDE"] == ["MAX", "MIN", "MIN", "MAX", "MAX"]


def test_actions_are_child_names_and_result_is_the_child():
    tree = small()
    assert tree.actions("A") == ["B", "C"]
    assert tree.actions("C") == []
    assert tree.result("A", "C") == "C"


@pytest.mark.parametrize("state, action", [("A", "D"), ("Z", "B"), ("C", "A")])
def test_result_rejects_moves_that_are_not_children(state, action):
    with pytest.raises(ValueError):
        small().result(state, action)


def test_leaves_are_terminal_with_utility_for_max_and_negated_for_min():
    tree = small()
    assert tree.is_terminal("D") and not tree.is_terminal("B")
    assert tree.utility("E", "MAX") == 3
    assert tree.utility("E", "MIN") == -3


def test_utility_of_an_internal_node_raises():
    with pytest.raises(ValueError, match="leaf"):
        small().utility("B", "MAX")


def test_subtree_starts_at_the_node_and_keeps_the_players():
    sub = small().subtree("B")
    assert sub.initial == "B"
    assert sub.to_move("B") == "MIN"
    assert sub.actions("B") == ["D", "E"]
    with pytest.raises(ValueError):
        small().subtree("Z")


@pytest.mark.parametrize(
    "children, leaves, root",
    [
        ({"A": ["B"]}, {"A": 1, "B": 2}, "A"),
        ({"A": ["B", "C"]}, {"B": 1}, "A"),
        ({"A": ["B", "C"], "B": ["C"]}, {"C": 1}, "A"),
        ({"A": ["B"]}, {"B": 1}, "Z"),
    ],
    ids=["leaf_with_children", "child_without_value", "two_parents", "unknown_root"],
)
def test_malformed_trees_are_rejected(children, leaves, root):
    with pytest.raises(ValueError):
        GameTree(children, leaves, root)


def test_result_and_utility_report_events():
    tree = small()
    with record() as trace:
        tree.utility(tree.result("A", "C"), "MAX")
    assert [(e.kind, e.data) for e in trace.events] == [
        ("result", {"state": "A", "action": "C"}),
        ("utility", {"state": "C"}),
    ]


def test_worked_tree_shape():
    assert shape(examples.worked_tree()) == (
        "A",
        [
            ("B", [("B1", 4), ("B2", 9), ("B3", 6)]),
            ("C", [("C1", 2), ("C2", 7), ("C3", 1)]),
            ("D", [("D1", 5), ("D2", 3), ("D3", 8)]),
        ],
    )


def test_minimax_exercise_shape():
    assert shape(examples.minimax_exercise()) == (
        "A",
        [
            ("B", [("D", [("H", 3), ("I", 7)]), ("E", [("J", 5), ("K", 1)])]),
            ("C", [("F", [("L", 2), ("M", 6)]), ("G", [("N", 9), ("O", 4)])]),
        ],
    )


def test_alpha_beta_exercise_shape():
    assert shape(examples.alpha_beta_exercise()) == (
        "A",
        [
            ("B", [("E", [("K", 3), ("L", 6)]), ("F", [("M", 7), ("N", 2)])]),
            ("C", [("G", [("O", 5), ("P", 8)]), ("H", [("Q", 1), ("R", 4)])]),
            ("D", [("I", [("S", 2), ("T", 1)]), ("J", [("U", 9), ("V", 6)])]),
        ],
    )


def test_ties_tree_shape():
    assert shape(examples.ties_tree()) == (
        "A",
        [("B", [("B1", 3), ("B2", 5)]), ("C", [("C1", 3), ("C2", 9)])],
    )


def test_evaluation_tree_is_the_worked_tree_with_evaluations():
    tree = examples.evaluation_tree()
    assert shape(tree) == shape(examples.worked_tree())
    assert tree.evaluations == {"B": 5, "C": 2, "D": 6}


def test_cutoff_tree_shape_and_evaluations():
    tree = examples.cutoff_tree()
    assert shape(tree) == (
        "A",
        [
            ("B", [("D", [("H", 5), ("I", 1)]), ("E", [("J", 8), ("K", 6)])]),
            ("C", [("F", [("L", 3), ("M", 2)]), ("G", [("N", 9), ("O", 7)])]),
        ],
    )
    assert tree.evaluations == {"A": 4, "B": 6, "C": 3, "D": 2, "E": 7, "F": 5, "G": 4}


def test_tree_evaluation_reads_the_evaluations_negated_for_min():
    tree = examples.cutoff_tree()
    assert tree_evaluation(tree, "B", "MAX") == 6
    assert tree_evaluation(tree, "B", "MIN") == -6
    with pytest.raises(ValueError, match="leaf"):
        tree_evaluation(tree, "H", "MAX")
    with pytest.raises(ValueError):
        tree_evaluation(examples.worked_tree(), "B", "MAX")


def test_random_game_tree_has_distinct_leaf_values_and_depends_on_the_seed():
    tree = examples.random_game_tree(3, 4, seed=1)
    assert sorted(tree.leaves.values()) == list(range(1, 82))
    assert all(len(tree.actions(node)) == 3 for node in tree.children)
    assert shape(examples.random_game_tree(3, 4, seed=1)) == shape(tree)
    assert shape(examples.random_game_tree(3, 4, seed=2)) != shape(tree)


def test_registry_of_examples():
    assert set(GAME_EXAMPLES) == {
        "worked_tree",
        "minimax_exercise",
        "alpha_beta_exercise",
        "ties_tree",
        "evaluation_tree",
        "cutoff_tree",
    }
    assert GAME_EXERCISES == {"minimax_exercise", "alpha_beta_exercise"}
    assert all(isinstance(make(), GameTree) for make in GAME_EXAMPLES.values())
