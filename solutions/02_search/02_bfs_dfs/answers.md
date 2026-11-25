**English** | [Polski](answers.pl.md)

# Lesson 2.2 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/02_search/02_bfs_dfs/README.md).

## Part A

### BFS

<!-- generated:trace-table algorithm=bfs example=exercise lang=en -->
| Step | Expanded node | Frontier (in removal order) | Reached set |
|---|---|---|---|
| 1 | A | B, C | A, B, C |
| 2 | B | C, D | A, B, C, D |
| 3 | C | D, F | A, B, C, D, F |
| 4 | D | F, E | A, B, C, D, E, F |
| 5 | F | E | A, B, C, D, E, F |

Goal **H** found while expanding **F**. Path: A → C → F → H.
<!-- /generated -->

Answers: `BFS_EXPANSION_ORDER = ["A", "B", "C", "D", "F"]` and `BFS_PATH = ["A", "C", "F", "H"]`.

BFS expands `D` before `F` because `D` entered the queue earlier. When it expands `F`, the state `E` has already been reached (the expansion of `D` added it), so it is ignored. `H`, on the other hand, is new and is a goal.

### DFS

<!-- generated:trace-table algorithm=dfs example=exercise lang=en -->
| Step | Popped node | Outcome | Frontier (in removal order) | Expanded |
|---|---|---|---|---|
| 1 | A | expanded | B, C | A |
| 2 | B | expanded | C, D, C | A, B |
| 3 | C | expanded | F, D, C | A, B, C |
| 4 | F | expanded | E, H, D, C | A, B, C, F |
| 5 | E | expanded | D, G, H, D, C | A, B, C, E, F |
| 6 | D | expanded | G, H, D, C | A, B, C, D, E, F |
| 7 | G | expanded | H, H, D, C | A, B, C, D, E, F, G |
| 8 | H | goal | H, D, C | A, B, C, D, E, F, G |

Path: A → B → C → F → E → G → H.
<!-- /generated -->

Answers: `DFS_EXPANSION_ORDER = ["A", "B", "C", "F", "E", "D", "G"]` and `DFS_PATH = ["A", "B", "C", "F", "E", "G", "H"]`.

Two things are worth noticing. After `F` is expanded, the goal `H` is on the stack, but under `E`, because `E` comes earlier in the alphabet. So DFS goes into `E` first. Then `D` turns out to be a dead end, because its neighbours are already expanded, and the algorithm backs up to `G`. The path found has 6 steps, while the shortest has only 3.

## Review questions

### 1. The early goal test in BFS

BFS generates nodes in order of non-decreasing depth. Before it generates the first node at depth *k* + 1, it has already expanded every node at depth *k*. If a goal lay shallower, it would have been generated earlier. So the first goal generated has the smallest possible number of steps, and waiting to test it until it leaves the frontier improves nothing. With different step costs this reasoning breaks down: a route with more steps can be cheaper. An early-generated goal then need not lie on the cheapest path, and the goal test has to move to the moment a node is removed from the frontier (lesson 2.3).

A good answer contains:

- the fact that BFS generates nodes in order of depth;
- the conclusion that the first goal generated has the smallest depth;
- the remark that with different costs, fewer steps do not mean a lower cost;
- the conclusion that the goal must then be tested when a node is removed from the frontier.

### 2. DFS memory

DFS without remembering states keeps only the current path and the not-yet-expanded neighbours of the nodes on it, about *b*·*m* nodes. BFS keeps the whole ripple, about *b*<sup>*d*</sup> nodes. DFS's advantage is huge on wide, deep trees. It disappears in graph search, because the set of expanded states grows with the number of states visited and can become as large as BFS's memory. It also shrinks when the maximum depth *m* is much larger than the goal depth *d*.

A good answer contains:

- the fact that DFS remembers only the path and the siblings of nodes on it;
- a comparison of O(*b*·*m*) with O(*b*<sup>*d*</sup>);
- the remark that remembering visited states takes this advantage away.

### 3. DFS on an infinite state space

If the state includes a counter that can grow without limit, every step leads to a new state. DFS can then descend ever deeper along one branch and never come back, even if a shallow goal exists in another branch. The set of visited states does not help, because no state ever repeats. So DFS is not complete. BFS will find a goal at a finite depth, as long as the branching factor is finite. The remedy is a depth limit or iterative deepening (lesson 2.6).

A good answer contains:

- a description of an infinite branch in which states never repeat;
- the remark that the set of visited states does not help here;
- the conclusion that DFS is not complete, while BFS is;
- at least one remedy.

### 4. Winding DFS routes

DFS does not know where the dock is: it searches without any information about the goal. It follows the first available action as far as it can and returns the first route it finds, not the shortest. So the shape of the route comes from the order of the actions (for example north first, then east), not from where the goal is. The robot circles whole blocks of shelves before it reaches the dock by chance.

A good answer contains:

- the remark that DFS uses no knowledge of where the goal is;
- the fact that it returns the first route found, not the shortest;
- the conclusion that the shape of the route depends on the order of actions.

### 5. The set of visited states in the warehouse

In a tree there is exactly one path to every state, so no state ever appears twice. In the warehouse, moves can be undone (north and then south returns to the same field), and there are cycles around blocks of shelves. Without a set of visited states DFS can walk back and forth forever, and BFS expands the same fields more and more often, so the number of expansions grows exponentially. The set guarantees that every state is expanded at most once.

A good answer contains:

- the fact that in a tree every state has a single path leading to it;
- the remark that the warehouse has cycles and reversible moves;
- what happens without the set: DFS goes round in circles, or BFS expands states many times;
- the conclusion that the set makes every state expanded at most once.

## Experiments

These are the results of the reference implementations. Your implementation may give a different number of expansions, for example if it tests for the goal at a different moment, but the overall picture should be the same.

| Map | Action order | BFS: route length | BFS: expansions | DFS: route length | DFS: expansions |
|---|---|---|---|---|---|
| `aisles` | N, E, S, W | 21 | 144 | 91 | 127 |
| `aisles` | W, S, E, N | 21 | 142 | 25 | 25 |
| `open_floor` | N, E, S, W | 10 | 89 | 138 | 141 |

- **Experiment 1.** BFS always finds the shortest route. With the order N, E, S, W, DFS first drives east, away from the dock, and finds a route more than four times longer.
- **Experiment 2.** The length of the BFS route does not change. With the order W, S, E, N, DFS heads in the right direction straight away: 25 steps with only 25 expansions. That is luck, not a merit of the algorithm.
- **Experiment 3.** In open space BFS floods the fields around the start until it reaches the nearby dock. DFS zigzags through almost the whole hall: its route has 138 steps, although 10 are enough.
