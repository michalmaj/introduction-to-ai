**English** | [Polski](answers.pl.md)

# Lesson 2.5 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/02_search/05_comparing_strategies/README.md).

## Part A

| | `complete_finite` | `complete_infinite` | `optimal_unit_costs` | `optimal_any_costs` |
|---|---|---|---|---|
| BFS | yes | yes | yes | no |
| DFS | yes | no | no | no |
| UCS | yes | yes | yes | yes |
| greedy | yes | no | no | no |
| A\* | yes | yes | yes | yes |

Justifications, column by column:

- **Completeness on a finite space.** All five algorithms are graph searches: they expand each state at most once (or, in UCS and A\*, again only when they find a cheaper way to it, and there are finitely many such improvements). On a finite space each of them eventually either finds the goal or empties the frontier and returns `None`.
- **Completeness on an infinite space.**
  - BFS explores the space layer by layer. The goal lies at a finite depth *d*, and every layer is finite because *b* is finite, so BFS reaches it.
  - UCS expands nodes in order of cost. There are finitely many nodes cheaper than *C*\*, because every step costs at least *ε*.
  - A\* expands only nodes with *f* ≤ *C*\*, and since *f* ≥ *g*, there are finitely many of them too.
  - DFS can go down an infinite branch in which states never repeat.
  - Greedy can go on forever after nodes that look ever closer to the goal, or equally close.
- **Optimality with equal costs.**
  - BFS finds the route with the fewest steps.
  - UCS and A\* find the cheapest route, and with equal costs the cheapest is the shortest.
  - DFS returns the first route it finds, for example a five-step route instead of a three-step one in lesson 2.2.
  - Greedy ignores the cost travelled so far: on the graph of lesson 2.4 it chose a route costing 12 instead of 7, and such counterexamples can be built with equal costs too.
- **Optimality with any costs.** Only UCS and A\* remain. BFS minimises the number of steps, not the cost; on the map `congested.txt` it paid 52 instead of 24.

## Review questions

### 1. Two different DFS

The DFS of lesson 2.2 remembers expanded states and never expands a state a second time. On a finite state space it can therefore make only finitely many expansions, after which it either finds the goal or empties the stack. The DFS of the worked example remembers nothing, so in a graph with a cycle it can return to the same states forever.

A good answer includes:

- the difference: a memory of expanded states, or none;
- the argument about the finite number of expansions;
- an example of a cycle in which DFS without memory loops.

### 2. An infinite space

Example: the state is an integer *n*. Two actions lead out of every state: "+1" and "goal", where "goal" leads to the goal state. If DFS tries "+1" first, it goes down the infinite branch 0, 1, 2, 3, … and never comes back. BFS expands layer by layer, so it finds the goal already at depth 1. The same pattern fits a warehouse whose state holds a counter of cells driven.

A good answer includes:

- an infinite branch in which states never repeat;
- an explanation of why DFS never comes back from it;
- an explanation of why BFS finds the shallow goal.

### 3. A\* and greedy

A\* orders the frontier by *g* + *h*. When *h* does not overestimate, a node on the cheapest path has *f* ≤ *C*\*, so it is removed before A\* returns a more expensive goal. If *h* overestimated, that node could wait in the frontier while A\* removed a more expensive goal first. Greedy does not consider *g*, what it has already paid, at all. Even a perfect heuristic does not help if the algorithm ignores the cost of the way it has already travelled.

A good answer includes:

- the role of admissibility in the optimality argument for A\*;
- the fact that greedy ignores *g*;
- the conclusion that a good heuristic alone is not enough for optimality.

### 4. DFS memory on the open floor

The formula O(*b*·*m*) says that the DFS frontier grows with the depth *m* the algorithm goes down to. On the open floor the DFS route has 138 steps, and every node on that path leaves a few unexplored neighbours on the stack. That gives 120 nodes in the frontier. BFS reaches the dock after 10 steps, and its wave has no time to grow. "DFS uses little memory" is true only when DFS does not go deep, and a graph search adds the set of expanded states on top.

A good answer includes:

- how the DFS frontier depends on the depth *m*;
- a comparison with the small depth of the goal for BFS;
- the conclusion that the advantage of DFS depends on the shape of the space.

### 5. Little memory, equal costs

The best choice is then iterative deepening (lesson 2.6). It remembers only the current path and its siblings, O(*b*·*d*), and with equal costs it finds the shortest route, like BFS. Reasonable answers also include BFS, if the map is small, or A\* with the Manhattan distance, if speed matters and memory suffices. The answer should, however, weigh memory and optimality, not only speed.

A good answer includes:

- a choice of algorithm justified by memory and optimality;
- the awareness that DFS saves memory but is not optimal;
- ideally: iterative deepening.

## Experiments

Results of the reference implementations. Your implementations may expand a slightly different number of cells if they break ties differently, but the route costs of UCS and A\* must be the same.

| Map | Algorithm | Steps | Cost | Expansions | Largest frontier |
|---|---|---|---|---|---|
| `congested` | BFS | 18 | 52 | 94 | 8 |
| `congested` | DFS | 22 | 24 | 22 | 4 |
| `congested` | UCS | 22 | 24 | 94 | 8 |
| `congested` | greedy | 18 | 52 | 18 | 4 |
| `congested` | A\* | 22 | 24 | 53 | 8 |
| `depot` | BFS | 32 | 50 | 137 | 6 |
| `depot` | DFS | 48 | 48 | 152 | 23 |
| `depot` | UCS | 38 | 38 | 150 | 9 |
| `depot` | greedy | 32 | 50 | 33 | 14 |
| `depot` | A\* | 38 | 38 | 124 | 16 |

- **Experiment 1.** UCS and A\* find the cheapest route, as the table says. BFS and greedy drive through the crowded aisle. On `depot.txt` DFS found a route cheaper than BFS (48 instead of 50), but that is down to the order of actions, not a guarantee: the table says what an algorithm promises on *every* map. A\* saves 41 cells on `congested.txt` but only 26 on `depot.txt`. On `depot.txt` as many as 125 cells have *f* ≤ 38, and 76 of them exactly *f* = 38: the regular grid of aisles offers plenty of equally cheap detours, and on ties in *f* A\* looks into almost all of them (the same effect as in experiment 3 of lesson 2.4). On `congested.txt` only 54 cells have *f* ≤ 24, because the storage area on the left is a dead end worth looking into only right next to the start.
- **Experiment 2.** The largest frontier of BFS and DFS:

  | Map | BFS | DFS |
  |---|---|---|
  | `aisles` | 12 | 23 |
  | `open_floor` | 17 | 120 |
  | `congested` | 8 | 4 |
  | `depot` | 6 | 23 |

  DFS has the smaller frontier only on `congested.txt`, where its route is short. On the open floor it goes 138 steps deep and keeps on the stack the siblings of almost every node on that path.
- **Experiment 3.** The number of expansions roughly doubles with every parcel: from 101 with one parcel to 7377 with six (with *h* = 0). On the logarithmic chart that is almost a straight line. With 20 parcels it would be of the order of 155 · 2<sup>20</sup>, more than 160 million states. The heuristic "number of parcels" helps hardly at all (6844 instead of 7377), because it is tiny compared with the true cost, which consists mostly of driving. You will design better heuristics in lesson 2.7. Really large problems, though, need other methods, described in module 4.
