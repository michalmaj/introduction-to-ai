**English** | [Polski](answers.pl.md)

# Lesson 2.3 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/02_search/03_uniform_cost_search/README.md).

## Part A

<!-- generated:trace-table algorithm=ucs example=weighted_exercise lang=en -->
| Step | Popped | g | f | Outcome | Frontier: state f, in removal order | Best known g |
|---|---|---|---|---|---|---|
| 1 | A | 0 | 0 | expanded | B 2, C 4 | A 0, B 2, C 4 |
| 2 | B | 2 | 2 | expanded | C 3, C 4, D 9 | A 0, B 2, C 3, D 9 |
| 3 | C | 3 | 3 | expanded | C 4, E 6, D 9 | A 0, B 2, C 3, D 9, E 6 |
| 4 | C | 4 | 4 | skipped | E 6, D 9 | A 0, B 2, C 3, D 9, E 6 |
| 5 | E | 6 | 6 | expanded | D 7, D 9, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 12, G 11 |
| 6 | D | 7 | 7 | expanded | F 8, D 9, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11 |
| 7 | F | 8 | 8 | expanded | D 9, H 10, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11, H 10 |
| 8 | D | 9 | 9 | skipped | H 10, G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11, H 10 |
| 9 | H | 10 | 10 | goal | G 11, F 12 | A 0, B 2, C 3, D 7, E 6, F 8, G 11, H 10 |

Goal **H** reached at cost 10. Path: A → B → C → E → D → F → H.
<!-- /generated -->

Answers: `UCS_EXPANSION_ORDER = ["A", "B", "C", "E", "D", "F"]` and `UCS_PATH = ["A", "B", "C", "E", "D", "F", "H"]`.

Three things are worth noticing:

- **Step 2.** Expanding `B` gives a way to `C` that costs 2 + 1 = 3, cheaper than the direct edge A–C, which costs 4. The entry C 4 becomes out of date and is skipped in step 4.
- **Step 5.** Expanding `E` gives a way to `D` that costs 6 + 1 = 7, cheaper than D 9 through `B`. That entry is skipped in step 8.
- **Step 7.** Expanding `F` generates the goal `H` at a cost of 10. Before UCS removes it, it still has to remove the out-of-date entry D 9, because 9 < 10.

The returned path has 6 steps and costs 2 + 1 + 3 + 1 + 1 + 2 = 10. The path through `G` (A → B → C → E → G → H) has only 5 steps, but costs 2 + 1 + 3 + 5 + 1 = 12. The most common mistake is to include the skipped entries of `C` and `D` in the expansion order.

## Part B

The reference solution skips out-of-date entries by comparing the cost of the removed node with the best known cost in reached. Two alternatives are correct as well:

- [aima_style.py](alternatives/aima_style.py) is the version from Russell and Norvig's textbook. It does not skip out-of-date entries but expands them once more. None of their children is cheaper than what is already known, so nothing new goes onto the frontier. The result is the same, and a few expansions are repeated;
- [expanded_set.py](alternatives/expanded_set.py) is Dijkstra's algorithm with a set of expanded states. Every child whose state has not been expanded yet goes onto the heap. The first time a state comes off the heap it already has its lowest cost, and later copies are skipped.

## Review questions

### 1. BFS with different costs

BFS expands nodes in order of the number of steps. The first route it finds has the fewest steps, but when steps have different costs, fewer steps does not mean cheaper: two expensive steps can cost more than four cheap ones. In the lesson's example BFS returns S → B → G with cost 12, while the cheapest route S → A → B → C → G costs 7.

A good answer includes:

- the fact that BFS orders nodes by the number of steps, not by cost;
- the observation that a route with fewer steps can be more expensive;
- an example.

### 2. Testing for the goal on removal

When a goal node is generated, the frontier may still hold a node through which the goal can be reached more cheaply. Only when the goal is removed from the frontier does every remaining node cost at least as much, and step costs are not negative, so no way through those nodes can be cheaper. Example: in the lesson's graph, expanding `B` generates `G` at a cost of 9, and an early goal test would return S → A → B → G. Yet `C`, with cost 5, is still waiting in the frontier and leads to `G` for 7.

A good answer includes:

- the observation that at generation time we do not know whether a cheaper way is waiting in the frontier;
- the argument that at removal time all remaining nodes are at least as expensive;
- a concrete example with numbers.

### 3. The counter on the heap

`heapq` compares tuples element by element. If two entries have the same cost, it compares the next element. Without a counter that would be the node, and `Node` objects cannot be compared, so the program would stop with a `TypeError`. The counter is different every time, so the comparison is always settled on it, in the order in which entries were added to the frontier.

A good answer includes:

- a description of how tuples are compared element by element;
- the consequence of having no counter: a `TypeError` when costs are equal;
- the fact that the counter breaks ties by the order of insertion.

### 4. Out-of-date entries

An out-of-date entry is a node that lies in the frontier even though a cheaper way to its state was found later. The cheaper node went onto the frontier too, and it is removed earlier. When we finally remove the old entry, its cost is higher than the one stored in reached. Everything that could be reached from it can be reached more cheaply from the newer node, which we have already expanded, so skipping it changes nothing.

A good answer includes:

- the definition: an entry whose cost is higher than the best known cost of its state;
- the observation that a cheaper node with the same state was removed and expanded earlier;
- the conclusion that expanding the old entry would give nothing cheaper.

### 5. UCS and BFS with equal costs

When every step costs the same, the cost of a path is proportional to its length, so UCS expands nodes in the same order of depth as BFS and finds a route of the same length. The difference lies in the goal test: BFS stops when the goal is generated, UCS only when it is removed from the frontier. So UCS usually expands more nodes, namely some of the nodes at the goal's depth as well. On top of that, heap operations are slower than those on a plain queue.

A good answer includes:

- the observation that with equal costs UCS expands nodes in order of depth, like BFS;
- the fact that both methods find routes of the same length;
- the conclusion that UCS expands more nodes because of the late goal test.

### 6. Zero and negative costs

With zero costs the optimality argument still works, because path costs do not decrease. The trouble is completeness: if the state space is infinite and some steps are free, UCS can keep expanding new states at the same cost forever and never reach the goal. That is why the completeness condition asks for every step to cost at least some *ε* > 0. With negative costs the optimality argument itself breaks: a goal removed from the frontier may later turn out to be reachable more cheaply, through a step with negative cost. When the graph has a cycle with negative cost, a cheapest way does not exist at all. Graphs with negative weights call for other algorithms, for example the Bellman-Ford algorithm.

A good answer includes:

- the observation that zero costs threaten termination on infinite spaces, not optimality;
- an explanation of why negative costs break the optimality argument;
- a mention of a negative-cost cycle or of another algorithm.

## Experiments

Results of the reference implementations. Your implementation may expand a slightly different number of cells if it breaks ties differently, but the route costs must be the same.

| Map | Algorithm | Steps | Cost | Expansions |
|---|---|---|---|---|
| `congested` | BFS | 18 | 52 | 94 |
| `congested` | UCS | 22 | 24 | 94 |

- **Experiment 1.** BFS drives straight along the corridor: 18 steps, but cost 52. UCS chooses the detour along the top aisle: 22 steps and cost 24. The UCS route crosses one slow cell, the first cell of the corridor, because that is the only way out of the start area into the aisles. Both algorithms expand 94 cells: BFS because the goal is 18 steps away and almost every cell of the map is closer; UCS because almost every cell can be reached for less than 24.
- **Experiment 2.** A corridor with *k* slow cells costs 18 + 2*k*, and the detour 22 (as long as the first corridor cell is ordinary). UCS drives along the corridor for *k* ≤ 2 and chooses the detour from *k* = 3 on. At *k* = 2 both routes cost 22; the reference UCS then picks the corridor, because on a tie it removes the node added first. Another implementation may pick the detour and is just as correct. At *k* = 17 the first corridor cell, which the detour goes through, is slow too, so the detour rises to 24.
- **Experiment 3.** UCS expanded 94 of the 104 free cells, including all 45 cells of the storage area on the left, even though the dock is on the right. The most expensive expanded node costs 24, as much as the route. UCS expands every cell that can be reached more cheaply than the goal, because it knows nothing about where the goal is: it spreads equally in every direction. An estimate of how far the dock is from a given cell would help. That is the heuristic of lesson 2.4.
