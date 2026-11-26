"""Mutant: a child's path_cost is only the cost of the last step.

Violated requirement: path_cost is the cost of the whole path from the root.
Common mistake in the lesson: "Only the last step's cost".
"""

from introai.search import Node, Problem

CAUGHT_BY = ("test_expand_accumulates_path_cost", "test_expand_uses_step_costs_of_the_map")

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise graph.
# Depth 1: B, C. Depth 2: the children of B (A, C, D) and of C (A, B, F).
# ---------------------------------------------------------------------------------------

TREE_NODES_AT_DEPTH_2: int | None = 6
STATES_AT_DEPTH_2: int | None = 5


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def expand(problem: Problem, node: Node) -> list[Node]:
    """The children of ``node``: one per action, in the order of ``problem.actions``."""
    children = []
    for action in problem.actions(node.state):
        next_state = problem.result(node.state, action)
        cost = problem.action_cost(node.state, action, next_state)
        children.append(Node(next_state, node, action, cost, node.depth + 1))
    return children


def count_tree_nodes(problem: Problem, depth: int) -> list[int]:
    """The number of search tree nodes at each depth 0, 1, ..., ``depth``."""
    level = [Node(problem.initial)]
    counts = [len(level)]
    for _ in range(depth):
        level = [child for node in level for child in expand(problem, node)]
        counts.append(len(level))
    return counts
