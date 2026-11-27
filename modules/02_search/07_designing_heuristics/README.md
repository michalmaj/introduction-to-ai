**English** | [Polski](README.pl.md)

# Lesson 2.7 — Designing heuristics

**Optional** · Requires: 2.5 Comparing search strategies (see the [course map](../../../COURSE_MAP.md)).

## Learning goals

After this lesson you will be able to:

- build a heuristic from a relaxed problem and explain why it is admissible;
- compare two heuristics with the notion of dominance;
- recognise a heuristic that overestimates and name a state where it does;
- design your own heuristic for the parcel pickup problem and see how much work it saves A\*.

## The problem

In lesson 2.5 A\* collected parcels in the warehouse with aisles. With every parcel the number of expansions roughly doubled, and the heuristic "number of parcels still on the floor" helped hardly at all: with six parcels, 6,844 expansions instead of 7,377. That heuristic counts only the picking up, while most of the cost is driving.

A better heuristic has to take distances into account. But carefully: if it overestimates even once, A\* may return a plan that is too long. How do you design heuristics that are strong and, at the same time, certainly admissible?

## Intuition

You get a good estimate by solving an **easier version** of the problem. If you remove some restriction, the robot has more options, so the cheapest solution of the easier problem cannot cost more than the solution of the real one. It is therefore a lower bound, that is, an admissible heuristic.

We reason this way in everyday life. "The shop is at least ten minutes away, because that is how long the walk straight across the park takes" is an estimate from an easier world in which you do not have to go around fences. The real time cannot be shorter.

## Formal model

### Relaxed problems

A **relaxed problem** comes from the real one by removing some of the restrictions on the actions. Every solution of the real problem is then also a solution of the relaxed problem, and an even cheaper one may appear. Hence:

$$h^*_{\text{relaxed}}(n) \le h^*(n),$$

so the exact cost of solving the relaxed problem is an admissible heuristic. What is more, it is consistent: in the relaxed problem the exact costs satisfy the triangle inequality, and every action of the real problem is also an action of the relaxed one.

To pay off, the relaxed problem must be **quick** to solve, ideally with a formula. Otherwise computing the heuristic costs more than it saves.

### Dominance

A heuristic *h*<sub>2</sub> **dominates** a heuristic *h*<sub>1</sub> if both are admissible and *h*<sub>2</sub>(*n*) ≥ *h*<sub>1</sub>(*n*) for every state. Then A\* with *h*<sub>2</sub> expands no more nodes than with *h*<sub>1</sub>, apart from ties. The reason: with a consistent heuristic A\* expands every node with *f*(*n*) < *C*\*, that is with *h*(*n*) < *C*\* − *g*(*n*). The larger *h*, the fewer nodes meet this condition.

**The maximum of heuristics.** When you have several admissible heuristics and none dominates the others, take their maximum: *h*(*n*) = max(*h*<sub>1</sub>(*n*), …, *h*<sub>k</sub>(*n*)). The maximum does not overestimate either, because none of its parts does, and it dominates each of them.

### The cost of a heuristic

A stronger heuristic saves expansions, but it costs something itself: you compute it for every generated node. A heuristic that looks at every pair of parcels makes a hundred comparisons per node with ten parcels. Usually that pays off, because every expansion saved means many fewer generated nodes, but it is worth measuring rather than assuming.

## Trace it by hand

### Worked example

Take the route problem of lesson 2.4: the robot drives to the dock, a move onto an ordinary cell costs 1 and onto a slow-zone cell 3. Let us relax it in three ways:

1. **The robot teleports.** Every cell can be reached with one free action, so the cost of getting there is 0. We get *h* = 0, that is UCS.
2. **The robot flies in a straight line.** There are no walls and no slow zones, and the robot can move in any direction. The cheapest route is a straight segment, so *h* is the **Euclidean distance**.
3. **The robot drives on the grid, but through walls.** The moves N, E, S, W remain, each costing 1, but obstacles and slow zones disappear. The cheapest route has as many moves as the **Manhattan distance**.

Each of these relaxed problems is closer to the real one than the previous, so it gives a larger estimate: 0 ≤ Euclidean distance ≤ Manhattan distance ≤ *h*\*. The Manhattan distance dominates the Euclidean, which dominates *h* = 0. The experiment of lesson 2.4 confirmed it: on the map with aisles A\* expanded 147 cells with *h* = 0, 66 with the Euclidean distance and 48 with the Manhattan distance.

### Your turn

Go back to the parcel pickup problem of lesson 1.3. The state is a pair (the robot's cell, the set of parcels still on the floor). A move onto a neighbouring free cell costs 1, and picking up a parcel (`PICK`) costs 1 too. Goal: collect all parcels. We write *M* for the Manhattan distance between cells.

Here are six candidate heuristics:

| Key | Heuristic |
|---|---|
| `h1` | the number of parcels still on the floor |
| `h2` | *M* from the robot to the nearest parcel, plus the number of parcels |
| `h3` | *M* from the robot to the farthest parcel, plus the number of parcels |
| `h4` | the sum of *M* from the robot to every parcel, plus the number of parcels |
| `h5` | *M* from the robot to the dock |
| `h6` | twice the number of parcels |

When there are no parcels left, the "nearest" and "farthest" parcel do not exist; that part is then 0. For each heuristic decide whether it is admissible, and write `True` or `False` in the dictionary `ADMISSIBLE` in Part A of `task.py`.

For an admissible heuristic, find the relaxed problem it comes from. For one that is not admissible, find a state in which it promises more than the robot really has to do.

## Common mistakes

1. **Summing the distances.** Adding up the distances to all parcels counts part of the way several times: driving to a farther parcel, the robot often passes closer ones. Such a heuristic overestimates.
2. **Multiplying by the number of parcels.** The distance to the nearest parcel times the number of parcels looks reasonable, but when parcels lie next to each other, the robot does not have to drive that far for each of them.
3. **Counting parcels only.** It is admissible, but adds almost nothing, because it leaves out driving, the largest part of the cost.
4. **No case for zero parcels.** Neither `max()` nor `min()` works on an empty set. In a goal state the heuristic must return 0, not raise an error.

The lesson's tests catch each of these mistakes.

## Task

### Part A: which heuristics are admissible

Fill in the dictionary `ADMISSIBLE` in `task.py` for the heuristics `h1`–`h6` in "Your turn".

### Part B: your own heuristic

Implement the function `parcel_heuristic(state)` in `task.py`, where `state = (robot cell, frozenset of parcels)`. The heuristic:

- returns 0 in a goal state, when there are no parcels left;
- never overestimates the true cost of collecting all parcels;
- makes A\* expand fewer nodes than with the heuristic "number of parcels".

Write the Manhattan distance function in `task.py` yourself, or copy yours from lesson 2.4. `task.py` does not import `introai.world.reference`.

### How to check

From the repository root:

```bash
uv run pytest modules/02_search/07_designing_heuristics
```

The admissibility test computes the exact cost of every reachable state on three small maps and compares it with your heuristic. If the heuristic overestimates anywhere, the message shows that state.

### Acceptance criteria

- All the lesson's tests pass.
- For your heuristic you can name a relaxed problem, or give another argument for why it does not overestimate.
- You can answer the review questions before you look at the answers.

## What the tests do not check

- **A proof of admissibility.** The tests check every state on three maps, but not on every possible map. A heuristic that passes the tests may overestimate elsewhere. The argument is yours to give.
- **Consistency.** The A\* of this course goes back to states when it finds a cheaper way, so admissibility is enough for it. The tests do not check whether your heuristic is also consistent.
- **The cost of computing the heuristic.** The tests count expansions, not time. A very expensive heuristic can save expansions and still slow the search down.

## Experiments

Open [experiments.ipynb](experiments.ipynb). Before each experiment write down your prediction, then check it:

1. How many expansions does A\* need with each heuristic, yours included, for 1–6 parcels? Which heuristic gives a plan that is too long?
2. Does *h*<sub>3</sub> dominate *h*<sub>2</sub> in every state? Does your heuristic dominate either of them?
3. Is the heuristic that saves the most expansions also the fastest?

## Review questions

1. Why does the exact cost of a relaxed problem never overestimate the cost of the real problem?
2. Which relaxed problem does the heuristic "number of parcels" come from? And the heuristic *h*<sub>3</sub>?
3. You have two admissible heuristics, neither of which dominates the other. How do you combine them so that the result is still admissible and no worse than either?
4. Give a state in which *h*<sub>6</sub> overestimates.
5. When can a stronger heuristic slow the search down, even though it reduces the number of expansions?

## If you get stuck

<details>
<summary>Hint 1: what the robot has to do</summary>

Before the robot is done, it must pick up every parcel (one action per parcel) and drive to each of them. What does the latter require at the very least? Which parcel does it certainly have to drive farthest to?

</details>

<details>
<summary>Hint 2: the goal state</summary>

When the set of parcels is empty, return 0 before you compute `max()` or `min()`. You can also use `max(..., default=0)`.

</details>

<details>
<summary>Hint 3: the test shows a state where you overestimate</summary>

Draw that state on the map: where the robot stands and where the parcels lie. Work out the shortest plan by hand and compare it with each part of your heuristic. One of them counts something twice.

</details>

## Key takeaways

- Heuristics are easiest to build from relaxed problems: remove a restriction, solve the easier problem, and its cost is admissible, even consistent.
- A dominating heuristic (larger, but still admissible) means fewer expansions.
- The maximum of admissible heuristics is admissible and dominates each of them.
- To show that a heuristic is not admissible, one state in which it overestimates is enough.
- A strong heuristic must also be cheap to compute.

## What next

- After your own attempt, compare with the solution and answers in [solutions/02_search/07_designing_heuristics/](../../../solutions/02_search/07_designing_heuristics/).
- Module 3 takes search into games. The evaluation function of a game position is a close relative of a heuristic.

## References

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, section 3.6 (heuristic functions, relaxed problems, dominance).
- J. Pearl, *Heuristics: Intelligent Search Strategies for Computer Problem Solving*, Addison-Wesley, 1984.
