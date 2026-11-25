"""Mutant: BFS tests only the children it generates, never the start state itself.

Violated requirement: when the start state is already a goal, return the root node.
Common mistake in the lesson: "Skipping the goal test on the start state".
"""

from collections import deque

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_bfs_returns_root_when_start_is_goal",)

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
    frontier = [Node(problem.initial)]  # LIFO stack: pop() takes the newest node
    expanded = set()  # every state we have already expanded

    while frontier:
        node = frontier.pop()
        if node.state in expanded:
            continue  # this state was reached again along another path
        if problem.is_goal(node.state):
            return node
        expanded.add(node.state)
        # Push in reverse order, so the child of the first action is popped first.
        for child in reversed(expand(problem, node)):
            if child.state not in expanded:
                frontier.append(child)

    return None
