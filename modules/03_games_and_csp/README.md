**English** | [Polski](README.pl.md)

# Module 3 — Games and constraint satisfaction

In module 2 the agent decided every step itself and looked for a sequence of actions leading to a goal. This module shows two kinds of problems where such a search is not enough. In **games** an opponent who wants to win moves in turn, so the agent needs a strategy for every reply. In **constraint satisfaction problems** (CSPs) what matters is not the path to a goal but the result itself: an assignment of values to variables that meets all the conditions at once. The games are tic-tac-toe and "four in a row" on a 5 × 5 board, where a mark can go on any empty cell. Constraint satisfaction takes us back to the warehouse: a delivery schedule has to be drawn up.

## Module goals

After this module you will be able to:

- describe a two-player game as a search problem and find the optimal move with minimax;
- prune the game tree with alpha-beta and measure how much that depends on the move order;
- stop a search at a given depth and design your own evaluation function for positions;
- describe a problem as variables, domains and constraints, and solve it with backtracking search, helped by heuristics and constraint propagation.

## Lessons

The list of the module's lessons, their prerequisites and their status are in the [course map](../../COURSE_MAP.md).

The module has two parts, which can be done in either order:

- **games, core lessons:** 3.1 → 3.2 → 3.3. After lesson 3.3 your program plays "four in a row" with your own evaluation function;
- **constraint satisfaction, core lessons:** 3.4 → 3.5. They need only lesson 2.5. They are in preparation;
- **optional lessons:** 3.6 on AC-3 constraint propagation (after 3.5), and 3.7 on games with chance and 3.8 on Monte Carlo tree search (both after 3.3). They are in preparation.

## Where this leads

- **Module 4, nature-inspired algorithms.** Local search scores states with an objective function, much as an evaluation function scores a game position, and does not look for a path to a goal. The delivery schedule of the constraint lessons returns there in lesson 4.5, solved with a genetic algorithm.
- **Module 8, reinforcement learning.** Monte Carlo tree search (lesson 3.8) chooses moves by weighing what is already known against what is still worth trying. The same dilemma of exploration and exploitation opens module 8.
