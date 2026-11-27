**English** | [Polski](answers.pl.md)

# Lesson 2.6 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/02_search/06_iterative_deepening/README.md).

## Part A

<!-- generated:trace-table algorithm=ids example=exercise lang=en -->
| Step | Limit | Popped (depth) | Outcome | Stack (top first) |
|---|---|---|---|---|
| 1 | 0 | A (0) | cut off | — |
| 2 | 1 | A (0) | expanded | B, C |
| 3 | 1 | B (1) | cut off | C |
| 4 | 1 | C (1) | cut off | — |
| 5 | 2 | A (0) | expanded | B, C |
| 6 | 2 | B (1) | expanded | A, C, D, C |
| 7 | 2 | A (2) | cut off | C, D, C |
| 8 | 2 | C (2) | cut off | D, C |
| 9 | 2 | D (2) | cut off | C |
| 10 | 2 | C (1) | expanded | A, B, F |
| 11 | 2 | A (2) | cut off | B, F |
| 12 | 2 | B (2) | cut off | F |
| 13 | 2 | F (2) | cut off | — |
| 14 | 3 | A (0) | expanded | B, C |
| 15 | 3 | B (1) | expanded | A, C, D, C |
| 16 | 3 | A (2) | cycle | C, D, C |
| 17 | 3 | C (2) | expanded | A, B, F, D, C |
| 18 | 3 | A (3) | cut off | B, F, D, C |
| 19 | 3 | B (3) | cut off | F, D, C |
| 20 | 3 | F (3) | cut off | D, C |
| 21 | 3 | D (2) | expanded | B, E, C |
| 22 | 3 | B (3) | cut off | E, C |
| 23 | 3 | E (3) | cut off | C |
| 24 | 3 | C (1) | expanded | A, B, F |
| 25 | 3 | A (2) | cycle | B, F |
| 26 | 3 | B (2) | expanded | A, C, D, F |
| 27 | 3 | A (3) | cut off | C, D, F |
| 28 | 3 | C (3) | cut off | D, F |
| 29 | 3 | D (3) | cut off | F |
| 30 | 3 | F (2) | expanded | C, E, H |
| 31 | 3 | C (3) | cut off | E, H |
| 32 | 3 | E (3) | cut off | H |
| 33 | 3 | H (3) | goal | — |

Goal **H** found with limit 3. Path: A → C → F → H.
<!-- /generated -->

Answer: `IDS_EXPANSIONS_PER_ITERATION = [0, 1, 3, 7]`.

In the round with limit 3 the expanded nodes are: `A`, `B`, `C` (through `B`), `D` (through `B`), `C` (straight from `A`), `B` (through `C`) and `F` (through `C`). Two things are worth noticing:

- **Cycles appear only with limit 3.** `A` at depth 2 (the paths A → B → A and A → C → A) is a cycle. With limit 2 the same node lies on the limit, and the limit is checked before the cycle, so it counts as cut off.
- **Redundant paths are not cycles.** `C` through `B` and `B` through `C` are states that appear in the tree a second time, but not on the same path. IDS expands them, because it remembers only the current path. This is exactly the cost that grows to thousands of expansions in the warehouse.

Typical mistakes: expanding cycle nodes (the last round then gives 9), counting cut-off nodes as expanded, or leaving out the round with limit 0.

## Part B

The reference solution uses a stack, like the DFS of lesson 2.2, and checks the conditions in the order: goal, limit, cycle. The alternative [recursive_dls.py](alternatives/recursive_dls.py) is the recursive version. The function calls itself for every child and passes a cutoff upwards: if any call returned `CUTOFF`, the whole branch returns `CUTOFF`. At the depths of this lesson recursion is safe, because Python's call stack has a limit of about 1000 levels.

## Review questions

### 1. `CUTOFF` and `None`

`CUTOFF` means: I found no goal with this limit, but I cut something off, so a goal may exist deeper down. `None` means: I cut nothing off and there is no goal anywhere. If both cases gave the same result, IDS would not know whether to search on. If both meant "search on", IDS would never stop on a finite graph with no goal. If both meant "stop", it would give up right after the round with limit 0.

A good answer includes:

- the meaning of both results;
- what goes wrong when they are merged one way or the other.

### 2. Why IDS finds the shortest route

The round with limit *L* applies the goal test to every node at depth at most *L*. If the round with limit *L* − 1 ended in a cutoff, then no state at depth less than *L* is a goal. A goal found in round *L* therefore lies at depth exactly *L*, and there is no shorter route. The order within a round (depth-first) does not matter; all that counts is that the rounds come in order.

A good answer includes:

- the observation that the limits grow one by one;
- the argument that the earlier round ruled out shallower goals;
- the conclusion about the shortest route with equal costs.

### 3. The cost of the repetition

Most nodes lie on the deepest level, and IDS goes through it only once. The shallower levels are repeated, but they are small: each is *b* times smaller than the next. The total work of IDS is roughly the work of BFS multiplied by 1 + 1/*b* + 1/*b*<sup>2</sup> + … = *b*/(*b* − 1). For *b* = 2 the ratio tends to 2: IDS expands about twice as many nodes as BFS. In the experiment with *d* = 8 it came out as 502 against 255, that is 1.97.

A good answer includes:

- the observation that the deepest level dominates and is gone through once;
- the geometric series or the formula *b*/(*b* − 1);
- the result for *b* = 2.

### 4. IDS in the warehouse

In a tree one path leads to every node, so IDS repeats only the shallow levels. In the warehouse very many paths without repeats lead to a cell (the redundant paths of lesson 2.1). IDS checks for cycles only on the current path, so it goes through each of those paths separately, and in every round. BFS remembers reached states and expands every cell once. On the open floor IDS expanded 9097 nodes against 89 for BFS.

A good answer includes:

- the difference: one path in a tree, many paths in a grid;
- the fact that IDS does not remember visited states;
- the conclusion that redundant paths multiply its work.

### 5. Memory for *b* = 10 and *d* = 10

IDS keeps on its stack the current path and the siblings of its nodes, about *b*·*d* = 100 nodes. BFS in the worst case keeps the whole wave at depth *d*, of the order of *b*<sup>*d*</sup> = 10<sup>10</sup> nodes. At a few dozen bytes per node that is hundreds of gigabytes, more than an ordinary computer has.

A good answer includes:

- the estimates O(*b*·*d*) for IDS and O(*b*<sup>*d*</sup>) for BFS;
- concrete numbers;
- the conclusion that BFS will not fit in memory.

## Experiments

Results of the reference implementations. The IDS expansion counts on trees do not depend on how the code is written; in the warehouse they may differ a little if your version orders the children differently.

| *b* | *d* | BFS | IDS | IDS / BFS | BFS frontier | IDS frontier |
|---|---|---|---|---|---|---|
| 2 | 8 | 255 | 502 | 1.97 | 255 | 9 |
| 3 | 8 | 3,280 | 4,916 | 1.50 | 6,559 | 17 |
| 4 | 8 | 21,845 | 29,124 | 1.33 | 65,533 | 25 |

| Map | Route steps | BFS | IDS (rounds) |
|---|---|---|---|
| `small` | 6 | 10 | 32 (7) |
| `aisles` | 21 | 144 | 3,497 (22) |
| `open_floor` | 10 | 89 | 9,097 (11) |
| `depot` | 32 | 137 | 12,388 (33) |

- **Experiment 1.** The work ratios tend to 2, 1.5 and 1.33, exactly *b*/(*b* − 1). The BFS frontier grows *b* times with every level, while the IDS frontier grows by only *b* − 1 nodes: for *b* = 3 and *d* = 8 that is 6,559 against 17.
- **Experiment 2.** In the warehouse IDS loses to BFS many times over: from 3 times on the small map to more than 100 times on the open floor. On the open floor the robot can drive in four directions from almost every cell, so the number of paths without repeats grows almost as fast as the tree of lesson 2.1. In the aisles there is less choice, so the chart grows more slowly. IDS pays off where there are few redundant paths and memory is short: in trees, and in huge spaces in which BFS would not fit in memory.
