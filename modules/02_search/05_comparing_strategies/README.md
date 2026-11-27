**English** | [Polski](README.pl.md)

# Lesson 2.5 — Comparing search strategies

**Core** · Requires: 2.4 Heuristics, greedy best-first search and A* (see the [course map](../../../COURSE_MAP.md)).

## Learning goals

After this lesson you will be able to:

- set out the properties of BFS, DFS, UCS, greedy and A\* side by side, and justify each of them;
- choose a strategy to fit the problem instead of always reaching for the same one;
- measure how much work and memory each algorithm uses on maps with costs;
- see where exact search stops being enough.

## The problem

The robot now knows five ways to look for a route. Which one should it take to work? There is no single answer. When all moves cost the same, BFS is perfectly good. When the warehouse has slow zones, BFS starts to overpay. A\* is usually the best, but only with a good heuristic. Greedy can be very fast, but it does not guarantee the cheapest route.

In this lesson you do not write a new algorithm. You gather what you already know into one table, and then test it in experiments on your own code from lessons 2.2–2.4.

## Intuition

All five algorithms do the same thing: take a node off the frontier, test it and expand it. They differ only in their answer to the question **which node to take next**. Each answer has its price:

- BFS takes the shallowest node. It never misses the shortest route, but it keeps the whole wave in memory.
- DFS takes the deepest. It goes down quickly, but it can run off into a very long route.
- UCS takes the cheapest. It finds the cheapest route, but it looks around in every direction.
- Greedy takes the one that looks closest to the goal. It is fast, but blind to cost.
- A\* takes the one with the smallest *g* + *h*. It combines the strengths of UCS and greedy, as long as the heuristic does not overestimate.

It is like choosing a means of transport: the fastest, the cheapest and the most comfortable are usually three different answers.

## Properties to compare

We take all the algorithms as written in this course: as graph searches that remember reached or expanded states. Step costs are always positive. The heuristic of A\* is admissible, while the heuristic of greedy may be any heuristic. We compare four properties:

| Key in `task.py` | Property | Assumptions |
|---|---|---|
| `complete_finite` | **completeness on a finite state space**: if a solution exists, the algorithm finds one; if none exists, it stops and returns `None` | there are finitely many states |
| `complete_infinite` | **completeness on an infinite state space**: the algorithm is sure to find a solution | there may be infinitely many states, but each state has finitely many actions, every step costs at least some *ε* > 0, and a solution exists |
| `optimal_unit_costs` | **optimality with equal costs**: the returned route has the fewest steps | every step costs the same |
| `optimal_any_costs` | **optimality with any costs**: the returned route is the cheapest | step costs are positive but may differ |

The answers follow from lessons 2.2–2.4. To write "no", one counterexample is enough: a map or a graph on which the algorithm fails. To write "yes", recall the argument for why the algorithm cannot fail.

## Time and memory

Notation as in the earlier lessons: *b* is the branching factor, *d* is the depth of the shallowest goal, *m* is the maximum depth, *C*\* is the cost of the optimal solution, and *ε* is the smallest step cost.

| Algorithm | Time in the worst case | Memory in the worst case |
|---|---|---|
| BFS | O(*b*<sup>*d*</sup>) | O(*b*<sup>*d*</sup>) |
| DFS | O(*b*<sup>*m*</sup>); as a graph search at most the number of states | O(*b*·*m*) for the frontier; the set of expanded states can grow to the number of states |
| UCS | O(*b*<sup>1 + ⌊*C*\*/*ε*⌋</sup>) | O(*b*<sup>1 + ⌊*C*\*/*ε*⌋</sup>) |
| Greedy | O(*b*<sup>*m*</sup>), usually much less with a good heuristic | as time |
| A\* | depends on the heuristic; expands every node with *f* < *C*\* | as time |

**How do we measure memory?** The simplest measure is the **largest size of the frontier** during the search. On top of it comes the set of reached states, which in a graph search grows up to the number of visited states. In the experiments we measure both expansions and the largest frontier.

Watch out with DFS. Its small memory, O(*b*·*m*), is an advantage only when *m*, the depth it goes down to, is small. On the open floor DFS can go more than a hundred steps deep, and then its frontier is larger than the BFS wave.

## How to choose a strategy

- **All steps cost the same, and the space is not huge:** BFS. It is simple and finds the shortest route.
- **Steps have different costs:** UCS, or A\* if you have an admissible heuristic. A\* finds the same route as UCS, but usually expands far fewer nodes.
- **Any route will do, as long as it comes quickly:** greedy with a good heuristic. Be prepared, though, for the route to cost much more.
- **Memory is short and the depth of the goal is unknown:** iterative deepening (lesson 2.6). It uses memory like DFS and finds the shortest route like BFS.
- **The state space is gigantic,** for example with dozens of parcels: none of these algorithms is enough. You need the approximate methods of module 4.

## Trace it by hand

### Worked example

There is no step-by-step trace here, because none of the algorithms is new. Instead we practise justifying properties. Take a sixth algorithm that is not in the table: **DFS that does not remember states**, the depth-first tree search of lesson 2.1.

- **Completeness on a finite space: no.** Counterexample: a graph with the cycle A–B–A. DFS without memory can go back and forth forever and never explore the rest of the graph.
- **Completeness on an infinite space: no.** The same counterexample works here, because the definition also allows a finite space: in a graph with a cycle in which a solution exists, DFS without memory can go round the cycle and never reach the solution.
- **Optimality with equal costs: no.** A counterexample without cycles: from the start `S` edges lead to `A` and `B`, from `A` to `C`, and from `C` and from `B` to the goal `G`. DFS that tries `A` first returns S → A → C → G (3 steps), although S → B → G (2 steps) exists.
- **Optimality with any costs: no.** If an algorithm is not optimal even when all costs are equal, it will not be optimal when costs differ either.

Notice the last step. Optimality with any costs implies optimality with equal costs, because equal costs are a special case of any costs. Completeness is not that simple. On a finite space the algorithm must also stop when there is no solution, and the definition of completeness on an infinite space does not require that. Each of these two properties has to be checked separately.

### Your turn

Fill in the table `PROPERTIES` in Part A of `task.py` for the five algorithms of this course: BFS, DFS, UCS, greedy and A\*. Remember that they are graph searches, not tree searches, so the answers for DFS differ from those in the example.

## Common mistakes

1. **Confusing DFS with tree search.** The DFS of the worked example remembers no states, while the DFS of lesson 2.2 remembers expanded states. They are two different algorithms with different properties. Check which one the table asks about.
2. **One answer for both kinds of space.** Completeness on a finite and on an infinite space are two different properties. An algorithm can have one and not the other, so look for a separate argument or counterexample for each.
3. **Mistaking speed for optimality.** That an algorithm reaches the goal quickly says nothing about the cost of the route it finds. Optimality has to be justified separately.
4. **Confusing steps with cost.** When steps have different costs, the route with the fewest steps need not be the cheapest. Check what exactly each algorithm minimises.

The lesson's tests catch each of these mistakes.

## Task

### Part A: the table of properties

In `task.py`, write `True` or `False` in each of the 20 fields of the table `PROPERTIES`. The exact meaning of each property and its assumptions are in the section "Properties to compare".

This lesson has no Part B. The notebook compares the algorithms you wrote in lessons 2.2–2.4.

### How to check

From the repository root:

```bash
uv run pytest modules/02_search/05_comparing_strategies
```

Each property has its own test. When something is wrong, the test says only how many of the five answers in that row are wrong, not which ones. That way you have to think the whole row through again.

### Acceptance criteria

- All the lesson's tests pass.
- You can justify every answer in the table with an argument or a counterexample.
- You can answer the review questions before you look at the answers.

## What the tests do not check

- **Justifications.** The test checks only the values in the table. Whether you know *why* is for the review questions to find out.
- **Conclusions from the experiments.** Compare your interpretation of the results with the answers in the solutions.
- **Running time.** The times in the notebook depend on the computer and are very small, so they vary from run to run.

## Experiments

Open [experiments.ipynb](experiments.ipynb). In `"mine"` mode the notebook runs your implementations from lessons 2.2, 2.3 and 2.4. If one of them does not work yet, switch to `"reference"`. Before each experiment, write down your prediction:

1. On the maps `congested.txt` and `depot.txt`: which algorithm finds the cheapest route, which expands the fewest cells, and which the most?
2. Which algorithm needs more memory, BFS or DFS? Does the answer depend on the map?
3. How much work does it take A\* to collect 1, 2, …, 6 parcels? What would happen with twenty?

## Review questions

1. How does the DFS of lesson 2.2 differ from the DFS of the worked example? How does that difference affect completeness on a finite state space?
2. Build an infinite state space in which a solution exists. Which of the five algorithms are sure to find it? Justify one "yes" and one "no".
3. Which part of the optimality argument for A\* uses the admissibility of the heuristic? Can the argument be carried over to greedy?
4. On the map `open_floor.txt` DFS has a larger frontier than BFS. How does that square with DFS "using little memory"?
5. You have a warehouse map without slow zones and very little memory. Which algorithm do you choose, and why?

## If you get stuck

<details>
<summary>Hint 1: where to start</summary>

Start with the UCS column. We proved all its properties in lesson 2.3. Then move on to BFS (lesson 2.2) and think about what changes when steps have different costs.

</details>

<details>
<summary>Hint 2: look for counterexamples</summary>

To answer "no", one graph on which the algorithm fails is enough. Good sources of counterexamples: the graphs of lessons 2.3 and 2.4, the map `congested.txt`, and an infinite space in which the state holds a counter that grows forever.

</details>

<details>
<summary>Hint 3: the properties depend on each other</summary>

An algorithm optimal with any costs is also optimal with equal costs. That lets you check whether the last two columns are consistent. Completeness is not that simple: on a finite space the algorithm must also stop when there is no solution.

</details>

## Key takeaways

- The five algorithms differ only in which node they take off the frontier next.
- Completeness and optimality depend on assumptions: a finite or infinite space, equal or different costs, an admissible or arbitrary heuristic.
- To write "yes" you need an argument; to write "no" one counterexample is enough.
- Speed, optimality and memory are three different criteria. No algorithm wins on all of them.
- Memory is a separate resource: we measure it by the largest frontier and the set of reached states.
- With many parcels the state space grows exponentially and exact search stops being enough.

## What next

- After your own attempt, compare with the answers in [solutions/02_search/05_comparing_strategies/](../../../solutions/02_search/05_comparing_strategies/).
- Optional lessons: 2.6 on iterative deepening and 2.7 on designing heuristics.
- Module 3 takes search into games, where an opponent moves too.

## References

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, sections 3.4–3.5 (comparing search strategies).
