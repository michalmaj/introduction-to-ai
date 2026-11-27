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


def test_astar_exercise_separates_ucs_a_star_and_greedy():
    from introai.search.examples import astar_exercise

    with record() as t:
        node = ucs(astar_exercise())
    assert expanded(t) == ["A", "C", "B", "E", "D", "F"] and node.path_cost == 8
    with record() as t:
        node = a_star(astar_exercise(), h_of("astar_exercise"))
    assert expanded(t) == ["A", "D", "B", "F"]
    assert node.states() == ["A", "B", "F", "G"] and node.path_cost == 8
    with record() as t:
        node = greedy_best_first(astar_exercise(), h_of("astar_exercise"))
    assert expanded(t) == ["A", "D"]
    assert node.states() == ["A", "D", "G"] and node.path_cost == 9


# --- Depth-limited search and iterative deepening -------------------------------------

from introai.search import CUTOFF  # noqa: E402
from introai.search.examples import cyclic, disconnected, exercise  # noqa: E402
from introai.search.reference import (  # noqa: E402
    depth_limited_search,
    iterative_deepening_search,
)


def expansions_per_iteration(problem):
    """Run IDS; return the number of expansions in each iteration and the result."""
    with record(kinds={"expand", "iteration"}) as t:
        node = iterative_deepening_search(problem)
    counts, current = [], 0
    for event in t.events:
        if event.kind == "expand":
            current += 1
        else:
            counts.append(current)
            current = 0
    return counts, node


@pytest.mark.parametrize(
    "make, counts, path",
    [
        (worked_example, [0, 1, 3, 3], ["S", "A", "C", "G"]),
        (exercise, [0, 1, 3, 7], ["A", "C", "F", "H"]),
        (binary_tree, [0, 1, 3, 7, 15], None),
        (cyclic, [0, 1, 3, 7, 11, 11], None),
    ],
    ids=["worked_example", "exercise", "binary_tree", "cyclic"],
)
def test_iterative_deepening_expansions_per_iteration(make, counts, path):
    found, node = expansions_per_iteration(make())
    assert found == counts
    assert (node.states() if node else None) == path


def test_depth_limited_search_results():
    assert depth_limited_search(worked_example(), 2) is CUTOFF
    assert depth_limited_search(disconnected(), 5) is None
    start_is_goal = GraphProblem.undirected([("A", "B")], "A", "A")
    assert depth_limited_search(start_is_goal, 0).states() == ["A"]
    assert iterative_deepening_search(start_is_goal).states() == ["A"]


def test_depth_limited_search_steps():
    with record() as t:
        depth_limited_search(worked_example(), 3)
    steps = [(e.data["popped"], e.data["depth"], e.data["outcome"]) for e in t.of_kind("step")]
    assert steps == [
        ("S", 0, "expanded"),
        ("A", 1, "expanded"),
        ("C", 2, "expanded"),
        ("A", 3, "cutoff"),
        ("B", 3, "cutoff"),
        ("G", 3, "goal"),
    ]
    first = t.of_kind("step")[0].data
    assert first["limit"] == 3 and first["stack"] == ["A", "B"]


def test_frontier_events_report_the_frontier_size():
    from introai.search.reference import a_star, dfs, ucs
    from introai.testing.search import max_frontier

    with record(kinds={"frontier"}) as t:
        bfs(worked_example())
    assert [e.data["size"] for e in t.of_kind("frontier")] == [2, 2, 2]
    assert max_frontier(t) == 2
    for run in (
        lambda p: dfs(p),
        lambda p: ucs(p),
        lambda p: a_star(p, lambda s: 0),
        lambda p: depth_limited_search(p, 3),
    ):
        with record(kinds={"frontier"}) as t:
            run(worked_example())
        assert max_frontier(t) > 0
    with record(kinds={"expand"}) as t:
        bfs(worked_example())
    assert max_frontier(t) == 0


def test_strategy_properties_table_is_consistent():
    from introai.search.reference import STRATEGY_PROPERTIES

    assert list(STRATEGY_PROPERTIES) == ["BFS", "DFS", "UCS", "greedy", "A*"]
    names = ["complete_finite", "complete_infinite", "optimal_unit_costs", "optimal_any_costs"]
    for row in STRATEGY_PROPERTIES.values():
        assert list(row) == names and all(isinstance(v, bool) for v in row.values())
        assert row["complete_finite"] or not row["complete_infinite"]
        assert row["optimal_unit_costs"] or not row["optimal_any_costs"]
    assert STRATEGY_PROPERTIES["UCS"]["optimal_any_costs"]
    assert not STRATEGY_PROPERTIES["BFS"]["optimal_any_costs"]
