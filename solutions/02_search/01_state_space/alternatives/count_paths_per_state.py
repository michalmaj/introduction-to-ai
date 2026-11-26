"""Alternative: count paths per state instead of building every node.

Nodes at the same depth with the same state have the same subtrees, so it is
enough to know how many of them there are. This stays fast for deep trees.
"""

from collections import Counter

from introai.search import Node, Problem

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
        children.append(Node(next_state, node, action, cost, node.depth + 1))
    return children


def count_tree_nodes(problem: Problem, depth: int) -> list[int]:
    """The number of search tree nodes at each depth 0, 1, ..., ``depth``."""
    level = Counter({problem.initial: 1})  # state -> number of nodes holding it
    counts = [1]
    for _ in range(depth):
        next_level: Counter = Counter()
        for state, paths in level.items():
            for action in problem.actions(state):
                next_level[problem.result(state, action)] += paths
        level = next_level
        counts.append(sum(level.values()))
    return counts
