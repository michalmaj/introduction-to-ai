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
