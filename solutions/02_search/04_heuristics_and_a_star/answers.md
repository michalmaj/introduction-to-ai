**English** | [Polski](answers.pl.md)

# Lesson 2.4 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/02_search/04_heuristics_and_a_star/README.md).

## Part A

### Greedy best-first search

<!-- generated:trace-table algorithm=greedy example=astar_exercise lang=en -->
| Step | Popped | g | f | Outcome | Frontier: state f, in removal order | Best known g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 7 | expanded | D 4, B 6, C 8 | A 0, B 2, C 1, D 3 |
| 2 | D | 3 | 4 | expanded | G 0, B 6, C 8 | A 0, B 2, C 1, D 3, G 9 |
| 3 | G | 9 | 0 | goal | B 6, C 8 | A 0, B 2, C 1, D 3, G 9 |

Goal **G** reached at cost 9. Path: A → D → G.
<!-- /generated -->

Answer: `GREEDY_PATH = ["A", "D", "G"]`.

After expanding `A`, the smallest *h* belongs to `D` (4), so greedy goes to `D` and from there straight to the goal. The route costs 3 + 6 = 9, while the cheapest one costs 8.

### A*

<!-- generated:trace-table algorithm=astar example=astar_exercise lang=en -->
| Step | Popped | g | f | Outcome | Frontier: state f, in removal order | Best known g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 7 | expanded | D 7, B 8, C 9 | A 0, B 2, C 1, D 3 |
| 2 | D | 3 | 7 | expanded | B 8, C 9, G 9 | A 0, B 2, C 1, D 3, G 9 |
| 3 | B | 2 | 8 | expanded | F 8, C 9, G 9 | A 0, B 2, C 1, D 3, F 6, G 9 |
| 4 | F | 6 | 8 | expanded | G 8, C 9, G 9 | A 0, B 2, C 1, D 3, F 6, G 8 |
| 5 | G | 8 | 8 | goal | C 9, G 9 | A 0, B 2, C 1, D 3, F 6, G 8 |

Goal **G** reached at cost 8. Path: A → B → F → G.
<!-- /generated -->

Answers: `ASTAR_EXPANSION_ORDER = ["A", "D", "B", "F"]` and `ASTAR_PATH = ["A", "B", "F", "G"]`.

A\* also expands `D` first, because it has the smallest *f* = 3 + 4 = 7. The goal generated then, however, has *f* = 9, and `B` only 2 + 6 = 8, so A\* does not stop but expands `B` and then `F`. Expanding `F` gives a cheaper way to the goal, with cost 8, and that entry is removed next. A\* never expands the states `C` and `E`: `C` has *f* = 1 + 8 = 9, more than the cost of the cheapest route.

The most common mistakes are comparing *h* alone instead of *f* = *g* + *h*, leaving `D` out of the expansion order (it is not on the returned path, but A\* expands it), and stopping at the first goal generated.

### For comparison: UCS

<!-- generated:trace-table algorithm=ucs example=astar_exercise lang=en -->
| Step | Popped | g | f | Outcome | Frontier: state f, in removal order | Best known g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 0 | expanded | C 1, B 2, D 3 | A 0, B 2, C 1, D 3 |
| 2 | C | 1 | 1 | expanded | B 2, E 2, D 3 | A 0, B 2, C 1, D 3, E 2 |
| 3 | B | 2 | 2 | expanded | E 2, D 3, F 6 | A 0, B 2, C 1, D 3, E 2, F 6 |
| 4 | E | 2 | 2 | expanded | D 3, F 6 | A 0, B 2, C 1, D 3, E 2, F 6 |
| 5 | D | 3 | 3 | expanded | F 6, G 9 | A 0, B 2, C 1, D 3, E 2, F 6, G 9 |
| 6 | F | 6 | 6 | expanded | G 8, G 9 | A 0, B 2, C 1, D 3, E 2, F 6, G 8 |
| 7 | G | 8 | 8 | goal | G 9 | A 0, B 2, C 1, D 3, E 2, F 6, G 8 |

Goal **G** reached at cost 8. Path: A → B → F → G.
<!-- /generated -->

UCS expands 6 nodes, including `C` and `E`, which lie in the opposite direction from the goal but are cheap. A\* expands only 4.

## Part B

The reference solution has one helper function `best_first(problem, f)`, which greedy and A\* call with different priorities. It is the UCS of lesson 2.3 with the path cost replaced by a priority function. Two alternatives are correct as well:

- [aima_style.py](alternatives/aima_style.py) does not skip out-of-date entries but expands them once more;
- [expanded_set.py](alternatives/expanded_set.py) expands each state at most once. For A\* this is correct when the heuristic is consistent, and the Manhattan distance in the warehouse is consistent.

## Review questions

### 1. Greedy and A*

Greedy best-first search orders the frontier by *h*, that is only by the estimate of the distance to the goal. A\* orders it by *g* + *h*, so it also takes into account how much the way has cost so far. Greedy can therefore choose a way that looks close to the goal but is expensive. In the lesson's example greedy goes from `S` to `B`, because *h*(`B`) = 3 < *h*(`A`) = 5, and returns a route that costs 12, while the cheapest costs 7. On the map `congested.txt` greedy drives along the corridor full of slow zones and pays 52 instead of 24.

A good answer includes:

- the priorities of both algorithms: *h* and *g* + *h*;
- an explanation that greedy ignores the cost of the way travelled so far;
- an example in which greedy returns a more expensive route.

### 2. The admissibility of the Manhattan distance

A heuristic is admissible if it never overestimates the true cost of reaching the goal: *h*(*n*) ≤ *h*\*(*n*). Every move of the robot changes the row or the column by 1, so reaching the dock takes at least as many moves as the Manhattan distance. Every move costs at least 1: an ordinary cell 1, a slow zone 3. So the true cost is at least the number of moves, and that is at least the Manhattan distance. Obstacles and slow zones can only raise the true cost.

A good answer includes:

- the definition *h*(*n*) ≤ *h*\*(*n*);
- the argument about the number of moves: every move changes the distance by at most 1;
- the argument about cost: every move costs at least 1.

### 3. Diagonal moves

No. One diagonal move changes the row and the column at the same time, so it reduces the Manhattan distance by 2 while costing only 1. A cell diagonally next to the dock has a Manhattan distance of 2 and a true cost of 1: the heuristic overestimates, so it is not admissible. In such a world the Chebyshev distance, max(|*r*<sub>1</sub> − *r*<sub>2</sub>|, |*c*<sub>1</sub> − *c*<sub>2</sub>|), is admissible, because that is the least number of moves needed when diagonal moves are allowed.

A good answer includes:

- the answer "no";
- an example of a cell for which the Manhattan distance overestimates;
- optionally: a heuristic that is admissible in such a world.

### 4. Non-decreasing f

When *n′* is a child of *n*, then *g*(*n′*) = *g*(*n*) + *c*(*n*, *a*, *n′*), so *f*(*n′*) = *g*(*n*) + *c* + *h*(*n′*). By consistency *c* + *h*(*n′*) ≥ *h*(*n*), so *f*(*n′*) ≥ *g*(*n*) + *h*(*n*) = *f*(*n*). Children therefore have an *f* at least as large as their parent's. The frontier always gives back the node with the smallest *f*, and new nodes have no smaller *f* than the one just removed, so the values removed one after another never decrease.

A good answer includes:

- the calculation *f*(*n′*) ≥ *f*(*n*) from the consistency inequality;
- the observation that the frontier always removes the smallest *f*;
- the conclusion that the *f* values expanded one after another never decrease.

### 5. Extreme heuristics

With *h* = 0 we get *f* = *g*, so A\* is exactly UCS. With *h* = *h*\*, the true cost to the goal, all nodes on the cheapest paths have *f* = *C*\* and all others a larger *f*. A\* then expands only nodes on the cheapest paths (when several paths are equally cheap, it may look at more than one of them). Such a heuristic, however, is as hard to compute as the solution itself.

A good answer includes:

- *h* = 0 gives UCS;
- *h* = *h*\* leads straight along the cheapest path;
- the observation that we usually do not know *h*\*.

### 6. An overestimating heuristic

A larger *h* makes A\* trust the estimate more and the travelled way less, and it behaves more and more like greedy. It then expands fewer nodes, because it rules out sooner the directions that look far away. But it loses the guarantee of optimality: it can remove a goal before exploring a cheaper way that the heuristic wrongly judged expensive. In experiment 2, the Manhattan distance times 3 cut the expansions from 53 to 18, but the route went up from 24 to 52. For A\* with the heuristic *w* · *h*, where *h* is admissible, the cost of the route is known to be at most *w* times the optimal one.

A good answer includes:

- the observation that a larger *h* means fewer expansions;
- the fact that overestimating takes away the guarantee of the cheapest route;
- an example, or a bound on how much more expensive the route can get.

## Experiments

Results of the reference implementations. Your implementation may expand a slightly different number of cells if it breaks ties differently, but the route costs of A\* with an admissible heuristic must be the same.

| Map | Algorithm and heuristic | Steps | Cost | Expansions |
|---|---|---|---|---|
| `congested` | UCS | 22 | 24 | 94 |
| `congested` | greedy, Manhattan | 18 | 52 | 18 |
| `congested` | A\*, *h* = 0 | 22 | 24 | 94 |
| `congested` | A\*, Euclidean | 22 | 24 | 53 |
| `congested` | A\*, Manhattan | 22 | 24 | 53 |
| `congested` | A\*, 2 × Manhattan | 22 | 24 | 32 |
| `congested` | A\*, 3 × Manhattan | 18 | 52 | 18 |
| `aisles` | UCS | 21 | 21 | 147 |
| `aisles` | A\*, Euclidean | 21 | 21 | 66 |
| `aisles` | A\*, Manhattan | 21 | 21 | 48 |
| `open_floor` | UCS | 10 | 10 | 104 |
| `open_floor` | A\*, Euclidean | 10 | 10 | 37 |
| `open_floor` | A\*, Manhattan | 10 | 10 | 34 |

- **Experiment 1.** Greedy drives along the corridor, because every step there reduces the Manhattan distance to the dock by 1. Greedy does not care about the cost of the steps. A\* takes the detour like UCS, but expands 53 cells instead of 94. In the storage area on the left it expands only 9 cells right next to the start: for example the cell `(3, 9)` has *g* = 1 and *h* = 19, so *f* = 20 < 24, while the cell `(3, 5)` has *g* = 5 and *h* = 23, so *f* = 28 > 24, and A\* never looks at it.
- **Experiment 2.** *h* = 0 is UCS. The Euclidean and the Manhattan distance are admissible, and both give the cheapest route. On this map they expand the same number of cells, because here the number of expansions is decided mainly by the cells near the start and by the aisles, not by the small differences between the two distances. The Manhattan distance times 2 is not admissible: in the cell right in front of the dock, for example, it gives 2 while the true cost is 1. Here A\* was lucky with it and still found the route for 24. Times 3, the heuristic outweighs the cost so much that A\* behaves like greedy and drives along the corridor for 52.
- **Experiment 3.** On both maps A\* with the Manhattan distance expands about three times fewer cells than UCS. On the open floor the Manhattan distance is almost equal to the true cost, while in the aisles the shelves force detours, so the heuristic underestimates the cost more. The Euclidean distance is never larger than the Manhattan distance, and both are admissible, so A\* with the Euclidean distance expands more cells: 66 instead of 48 in the aisles. A larger admissible heuristic means less work. We say that the Manhattan distance dominates the Euclidean distance (lesson 2.7).
