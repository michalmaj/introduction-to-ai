"""Mutant: children are created without a parent, so every child looks like a root.

Violated requirement: each child points to the node it was expanded from.
Common mistake in the lesson: "A child without a parent".
"""

from introai.search import Node, Problem

CAUGHT_BY = ("test_expand_records_parent_and_action",)

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
        cost = node.path_cost + problem.action_cost(node.state, action, next_state)
        children.append(Node(next_state, None, action, cost, node.depth + 1))
    return children


def count_tree_nodes(problem: Problem, depth: int) -> list[int]:
    """The number of search tree nodes at each depth 0, 1, ..., ``depth``."""
    level = [Node(problem.initial)]
    counts = [len(level)]
    for _ in range(depth):
        level = [child for node in level for child in expand(problem, node)]
        counts.append(len(level))
    return counts
