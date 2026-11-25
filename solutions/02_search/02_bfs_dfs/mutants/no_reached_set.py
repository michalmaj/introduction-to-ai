"""Mutant: neither search remembers which states it has already reached or expanded.

Violated requirement: a graph search expands every state at most once (and stops on
graphs with cycles).
Common mistake in the lesson: "No record of visited states".
"""

from collections import deque

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_bfs_expands_each_state_at_most_once", "test_dfs_expands_each_state_at_most_once")

# ---------------------------------------------------------------------------------------
# Part A: answers for the exercise graph.
# ---------------------------------------------------------------------------------------

BFS_EXPANSION_ORDER: list[str] | None = ["A", "B", "C", "D", "F"]
BFS_PATH: list[str] | None = ["A", "C", "F", "H"]
DFS_EXPANSION_ORDER: list[str] | None = ["A", "B", "C", "F", "E", "D", "G"]
DFS_PATH: list[str] | None = ["A", "B", "C", "F", "E", "G", "H"]


# ---------------------------------------------------------------------------------------
# Part B: implementation.
# ---------------------------------------------------------------------------------------


def bfs(problem: Problem) -> Node | None:
    """Breadth-first search: always expand the shallowest node in the frontier."""
    root = Node(problem.initial)
    if problem.is_goal(root.state):
        return root

    frontier = deque([root])  # FIFO queue: popleft() takes the oldest node

    while frontier:
        node = frontier.popleft()
        for child in expand(problem, node):
            if problem.is_goal(child.state):  # early goal test: safe for BFS
                return child
            frontier.append(child)

    return None


def dfs(problem: Problem) -> Node | None:
    """Depth-first search: always expand the deepest node in the frontier."""
    frontier = [Node(problem.initial)]  # LIFO stack: pop() takes the newest node

    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        # Push in reverse order, so the child of the first action is popped first.
        for child in reversed(expand(problem, node)):
            frontier.append(child)

    return None
