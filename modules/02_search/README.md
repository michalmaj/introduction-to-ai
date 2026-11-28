**English** | [Polski](README.pl.md)

# Module 2 — Search

How do you find a way from the initial state to a goal when all you know is which actions are available and where they lead? This module covers strategies for searching a state space: from breadth-first and depth-first search, through taking step costs into account, to heuristics and the A* algorithm. The tasks take place in the warehouse, where the robot looks for a route to the dock.

## Module goals

After this module you will be able to:

- formulate a problem as a search through a state space;
- implement and trace BFS, DFS, uniform-cost search, greedy best-first search and A*;
- compare strategies in terms of completeness, optimality, time and memory;
- design a heuristic and judge whether it is admissible.

## Lessons

The module's lessons, their dependencies and their status are listed in the [course map](../../COURSE_MAP.md).

The order of lessons in the module:

- **core lessons:** 2.1 → 2.2 → 2.3 → 2.4 → 2.5. After lesson 2.5 you know five search strategies and when to use each;
- **optional lessons:** 2.6 on iterative deepening and 2.7 on designing heuristics. Both need only lesson 2.5 and can be done in either order.

## Where this leads

- **[Module 3](../03_games_and_csp/README.md), games and constraint satisfaction.** Search in which an opponent moves too. The evaluation function of a game position is a close relative of the heuristics of lessons 2.4 and 2.7.
- **Module 4, nature-inspired algorithms.** When the robot has to collect many parcels, the state space grows exponentially and exact search is no longer enough. You will see how to find a good, though not necessarily the best, route in reasonable time.
- **Module 8, reinforcement learning.** A* assumes we know the model of the world. Q-learning teaches the robot to reach its goal without that knowledge.
