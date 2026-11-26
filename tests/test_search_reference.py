import pytest

from introai.search.examples import EXAMPLES, binary_tree, worked_example
from introai.search.problems import GraphProblem
from introai.search.reference import bfs, dfs
from introai.trace import record


def expanded(trace):
    return [e.data["node"].state for e in trace.of_kind("expand")]


@pytest.mark.parametrize(
    "name, algo, exp_order, exp_path",
    [
        ("worked_example", bfs, ["S", "A", "B", "C"], ["S", "A", "C", "G"]),
        ("worked_example", dfs, ["S", "A", "C", "B", "D"], ["S", "A", "C", "B", "D", "G"]),
        ("exercise", bfs, ["A", "B", "C", "D", "F"], ["A", "C", "F", "H"]),
        (
            "exercise",
            dfs,
            ["A", "B", "C", "F", "E", "D", "G"],
            ["A", "B", "C", "F", "E", "G", "H"],
        ),
        ("disconnected", bfs, ["A", "B"], None),
        ("disconnected", dfs, ["A", "B"], None),
        ("cyclic", bfs, ["A", "B", "C", "D"], None),
        ("cyclic", dfs, ["A", "B", "C", "D"], None),
    ],
)
def test_reference_orders_and_paths(name, algo, exp_order, exp_path):
    with record() as t:
        node = algo(EXAMPLES[name]())
    assert expanded(t) == exp_order
    assert (node.states() if node else None) == exp_path


def test_binary_tree_full_traversal_orders():
    with record() as t:
        bfs(binary_tree())
    assert expanded(t) == list("RABCDEFGHIJKLMN")
    with record() as t:
        dfs(binary_tree())
    assert expanded(t) == list("RACGHDIJBEKLFMN")


def test_start_is_goal_returns_root_without_expansion():
    p = GraphProblem.undirected([("A", "B")], "A", "A")
    for algo in (bfs, dfs):
        with record() as t:
            node = algo(p)
        assert node.states() == ["A"] and expanded(t) == []


def test_bfs_step_events_worked_example():
    with record() as t:
        bfs(worked_example())
    steps = [(e.data["expanded"], e.data["frontier"], e.data["reached"]) for e in t.of_kind("step")]
    assert steps == [
        ("S", ["A", "B"], ["A", "B", "S"]),
        ("A", ["B", "C"], ["A", "B", "C", "S"]),
        ("B", ["C", "D"], ["A", "B", "C", "D", "S"]),
        ("C", ["D"], ["A", "B", "C", "D", "S"]),
    ]
    assert t.of_kind("goal")[0].data["node"].state == "G"


def test_dfs_step_events_worked_example():
    with record() as t:
        dfs(worked_example())
    steps = [(e.data["popped"], e.data["outcome"], e.data["frontier"]) for e in t.of_kind("step")]
    assert steps == [
        ("S", "expanded", ["A", "B"]),
        ("A", "expanded", ["C", "B"]),
        ("C", "expanded", ["B", "G", "B"]),
        ("B", "expanded", ["D", "G", "B"]),
        ("D", "expanded", ["G", "G", "B"]),
        ("G", "goal", ["G", "B"]),
    ]
    assert t.of_kind("step")[3].data["expanded"] == ["A", "B", "C", "S"]


def test_dfs_reports_skipped_pops():
    with record() as t:
        dfs(EXAMPLES["cyclic"]())
    outcomes = [e.data["outcome"] for e in t.of_kind("step")]
    assert outcomes.count("expanded") == 4 and "skipped" in outcomes


def test_reference_skips_step_events_when_not_wanted():
    with record() as full:
        bfs(worked_example())
    with record(kinds={"expand"}) as lean:
        bfs(worked_example())
    assert lean.of_kind("step") == [] and lean.of_kind("goal") == []
    assert expanded(lean) == expanded(full)


# --- UCS, greedy best-first and A* ---------------------------------------------------

from introai.search.examples import HEURISTICS, weighted_example, weighted_exercise  # noqa: E402
from introai.search.reference import a_star, greedy_best_first, ucs  # noqa: E402


def h_of(name):
    table = HEURISTICS[name]
    return lambda state: table[state]


def outcomes(trace):
    return [(e.data["popped"], e.data["outcome"]) for e in trace.of_kind("step")]


def test_ucs_worked_example():
    with record() as t:
        node = ucs(weighted_example())
    assert expanded(t) == ["S", "A", "B", "C"]
    assert node.states() == ["S", "A", "B", "C", "G"] and node.path_cost == 7
    assert outcomes(t)[-2:] == [("B", "skipped"), ("G", "goal")]


def test_ucs_exercise():
    with record() as t:
        node = ucs(weighted_exercise())
    assert expanded(t) == ["A", "B", "C", "E", "D", "F"]
    assert node.states() == ["A", "B", "C", "E", "D", "F", "H"] and node.path_cost == 10
    assert [s for s, outcome in outcomes(t) if outcome == "skipped"] == ["C", "D"]


def test_a_star_worked_example_and_exercise():
    with record() as t:
        node = a_star(weighted_example(), h_of("weighted_example"))
    assert expanded(t) == ["S", "A", "B", "C"] and node.path_cost == 7
    with record() as t:
        node = a_star(weighted_exercise(), h_of("weighted_exercise"))
    assert expanded(t) == ["A", "B", "C", "E", "D", "F"] and node.path_cost == 10
    assert node.states() == ["A", "B", "C", "E", "D", "F", "H"]


def test_greedy_worked_example():
    with record() as t:
        node = greedy_best_first(weighted_example(), h_of("weighted_example"))
    assert expanded(t) == ["S", "B"]
    assert node.states() == ["S", "B", "G"] and node.path_cost == 12


def test_bfs_ignores_costs_on_the_weighted_example():
    node = bfs(weighted_example())
    assert node.states() == ["S", "B", "G"] and node.path_cost == 12


def test_best_first_start_is_goal_and_unreachable():
    p = GraphProblem.undirected([("A", "B")], "A", "A")
    assert ucs(p).states() == ["A"]
    assert ucs(EXAMPLES["disconnected"]()) is None
    assert a_star(EXAMPLES["disconnected"](), lambda s: 0) is None


def test_step_events_carry_costs():
    with record() as t:
        ucs(weighted_example())
    first = t.of_kind("step")[0].data
    assert (first["g"], first["f"], first["frontier"]) == (0, 0, [("A", 1), ("B", 6)])
    assert first["reached"] == [("A", 1), ("B", 6), ("S", 0)]


def test_count_tree_nodes_counts_every_path():
    from introai.search.examples import binary_tree, cyclic, worked_example
    from introai.search.reference import count_tree_nodes

    assert count_tree_nodes(binary_tree(), 4) == [1, 2, 4, 8, 0]
    assert count_tree_nodes(worked_example(), 3) == [1, 2, 5, 12]
    assert count_tree_nodes(cyclic(), 0) == [1]
    assert count_tree_nodes(cyclic(), 2) == [1, 2, 6]  # A -> B, C -> (A, C, D), (A, B, D)


def test_reference_expand_is_the_course_expand():
    from introai.search import expand, reference

    assert reference.expand is expand
