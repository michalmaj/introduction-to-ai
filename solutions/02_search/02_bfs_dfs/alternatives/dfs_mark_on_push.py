"""Alternative: DFS that marks states as reached when it pushes them, so nothing is skipped
when popping.
"""

from collections import deque

from introai.search import Node, Problem, expand

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
    root = Node(problem.initial)
    frontier = [root]
    reached = {root.state}

    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in reversed(expand(problem, node)):
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)

    return None
