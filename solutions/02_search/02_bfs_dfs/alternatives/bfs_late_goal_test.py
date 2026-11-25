"""Alternative: BFS that tests for the goal when a node leaves the frontier.

Slower than the early goal test, but just as correct for unit step costs.
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
    frontier = deque([Node(problem.initial)])
    reached = {problem.initial}

    while frontier:
        node = frontier.popleft()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            if child.state not in reached:
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
