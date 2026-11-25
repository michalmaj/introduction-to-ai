"""Mutant: BFS takes nodes from the end of the frontier, so it behaves like a stack.

Violated requirement: BFS expands nodes in order of depth (a FIFO frontier).
Common mistake in the lesson: "A stack instead of a queue in BFS".
"""

from collections import deque

from introai.search import Node, Problem, expand

CAUGHT_BY = ("test_bfs_expands_in_nondecreasing_depth",)

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
        node = frontier.pop()  # BUG: takes the newest node, not the oldest
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
