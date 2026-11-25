"""Mutant: a recursive DFS that does not remember which states it has expanded.

On a graph with cycles it recurses back and forth until Python's recursion limit.
Violated requirement: a graph search expands every state at most once.
Common mistake in the lesson: "No record of visited states".
"""

from collections import deque

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_dfs_expands_each_state_at_most_once",)

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
    reached = {root.state}  # every state we have already put in the frontier

    while frontier:
        node = frontier.popleft()
        for child in expand(problem, node):
            if child.state in reached:
                continue
            if problem.is_goal(child.state):  # early goal test: safe for BFS
                return child
            reached.add(child.state)
            frontier.append(child)

    return None


def dfs(problem: Problem) -> Node | None:
    """Depth-first search: always expand the deepest node in the frontier."""

    def visit(node: Node) -> Node | None:
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):  # BUG: no record of expanded states
            found = visit(child)
            if found is not None:
                return found
        return None

    return visit(Node(problem.initial))
