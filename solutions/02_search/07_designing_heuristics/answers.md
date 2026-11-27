**English** | [Polski](answers.pl.md)

# Lesson 2.7 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/02_search/07_designing_heuristics/README.md).

## Part A

| Heuristic | Admissible | Justification |
|---|---|---|
| `h1`: number of parcels | yes | Relaxed problem: the robot picks parcels up from anywhere, without driving. Only the `PICK` actions remain, one per parcel. |
| `h2`: nearest parcel + number of parcels | yes | The robot has to reach at least the first parcel it picks up, and that one is at least as far as the nearest. Driving on a grid without walls takes at least *M* moves. Add one `PICK` per parcel. |
| `h3`: farthest parcel + number of parcels | yes | The robot has to stand on the farthest parcel at some point, and getting there takes at least *M* moves, whatever the order. Add the `PICK` actions. |
| `h4`: sum of distances + number of parcels | no | Counterexample: the robot at (1, 1), parcels at (1, 2) and (1, 3). Four actions are enough: E, PICK, E, PICK. The heuristic gives 1 + 2 + 2 = 5. On the map `parcels.txt` in the initial state it gives 13, while the shortest plan has 11 actions. |
| `h5`: distance to the dock | no | The goal does not require driving to the dock. In a goal state with the robot far from the dock, the true cost is 0 while the heuristic is positive. |
| `h6`: twice the number of parcels | no | The robot stands on the last parcel: one `PICK` is enough, while the heuristic gives 2. |

Notice the chain of dominance: *h*<sub>1</sub> ≤ *h*<sub>2</sub> ≤ *h*<sub>3</sub> in every state, because the farthest parcel is at least as far as the nearest.

## Part B

The reference solution is *h*<sub>3</sub>: the distance to the farthest parcel plus the number of parcels. Two alternatives pass the tests as well:

- [nearest_parcel.py](alternatives/nearest_parcel.py) is *h*<sub>2</sub>. It is admissible but weaker: *h*<sub>3</sub> dominates it, so A\* expands more nodes with it.
- [nearest_plus_spread.py](alternatives/nearest_plus_spread.py) is the strongest of the three. The robot first drives to some parcel, at least the nearest one. Afterwards it has to visit both parcels of the farthest-apart pair, which takes at least their distance. The sum of these two parts and the number of parcels does not overestimate. It dominates *h*<sub>3</sub>, because by the triangle inequality *M*(robot, farthest) ≤ *M*(robot, nearest) + *M*(nearest, farthest). With six parcels A\* expands 657 nodes with it instead of 1,814.

## Review questions

### 1. Why a relaxed problem does not overestimate

A relaxed problem has the same states and at least the same actions as the real one, and some restrictions disappear. Every plan of the real problem is therefore also a plan of the relaxed problem, at the same or a lower cost. The cheapest plan of the relaxed problem cannot cost more than the cheapest plan of the real one.

A good answer includes:

- the observation that every real plan is also a relaxed plan;
- the conclusion that the relaxed optimum is no larger than the real one.

### 2. An argument for an admissible heuristic

Each of the three admissible heuristics has a simple argument. *h*<sub>1</sub> is the cost of a relaxed problem in which the robot picks parcels up without driving, for example from anywhere. For *h*<sub>2</sub> and *h*<sub>3</sub> a lower bound is the simplest. Before the robot is done, it has to stand on every parcel, so it has to drive at least the Manhattan distance to the nearest parcel (*h*<sub>2</sub>), and even to the farthest one (*h*<sub>3</sub>), because there is no shorter way on the grid even without walls. Add one `PICK` per parcel. A relaxed problem for *h*<sub>3</sub> would depend on the state, because the farthest parcel changes as the robot drives, which is why the lower-bound argument is simpler here.

A good answer includes:

- the choice of a heuristic that really is admissible;
- a relaxed problem or a lower bound on the cost;
- the `PICK` actions taken into account.

### 3. Combining heuristics

Take the maximum: *h*(*n*) = max(*h*<sub>a</sub>(*n*), *h*<sub>b</sub>(*n*)). In every state the maximum equals one of the admissible heuristics, so it does not overestimate. It is also greater than or equal to each of them, so it dominates both. The sum would not be safe, because two correct lower bounds may count the same part of the cost.

A good answer includes:

- the maximum as the way to combine;
- a justification of admissibility and dominance;
- optionally: a warning against the sum.

### 4. A state in which a heuristic overestimates

For each of the three heuristics that are not admissible, one state is enough:

- *h*<sub>4</sub>: the robot at (1, 1), parcels at (1, 2) and (1, 3). Four actions are enough, while the heuristic gives 5;
- *h*<sub>5</sub>: a goal state (all parcels collected) with the robot far from the dock. The true cost is 0, while the heuristic is positive;
- *h*<sub>6</sub>: the robot stands on the cell of the last parcel. The true cost is 1, a single `PICK`, while the heuristic gives 2.

A good answer includes:

- the choice of a heuristic that really is not admissible;
- a concrete state;
- the true cost and the value of the heuristic in that state.

### 5. When a stronger heuristic slows things down

When computing it for one node costs more than the reduced number of expansions saves. For example, a heuristic that solves a hard subproblem for every state (say, the exact tour through all parcels) may expand very few nodes and still run longer than a simple distance. In experiment 3 the stronger heuristics were also faster, because they are cheap to compute, but that need not always be so.

A good answer includes:

- a comparison of the cost of computing the heuristic with the work it saves;
- an example of a heuristic that is expensive to compute.

## Experiments

Results of the reference implementation on the map with aisles (expansions / plan length). Your heuristic gives different numbers if it differs from *h*<sub>3</sub>.

| Parcels | *h* = 0 | *h*<sub>1</sub> | *h*<sub>2</sub> | *h*<sub>3</sub> | *h*<sub>4</sub> |
|---|---|---|---|---|---|
| 1 | 101 / 14 | 89 / 14 | 18 / 14 | 18 / 14 | 18 / 14 |
| 2 | 181 / 19 | 159 / 19 | 51 / 19 | 36 / 19 | 23 / 19 |
| 3 | 803 / 42 | 767 / 42 | 476 / 42 | 262 / 42 | 112 / **46** |
| 4 | 1,815 / 51 | 1,697 / 51 | 1,159 / 51 | 635 / 51 | 324 / **55** |
| 5 | 3,672 / 56 | 3,488 / 56 | 2,395 / 56 | 1,071 / 56 | 440 / **72** |
| 6 | 7,377 / 57 | 6,844 / 57 | 4,844 / 57 | 1,814 / 57 | 583 / **81** |

- **Experiment 1.** The order from most to fewest expansions: *h* = 0, *h*<sub>1</sub>, *h*<sub>2</sub>, *h*<sub>3</sub>, *h*<sub>4</sub>. *h*<sub>4</sub> expands the fewest because it overestimates: A\* believes it and rushes to the goal, but from three parcels on it returns plans that are too long (81 actions instead of 57 with six parcels). With six parcels *h*<sub>3</sub> expands 1,814 nodes and *h*<sub>2</sub> 4,844, that is 2.7 times as many.
- **Experiment 2.** *h*<sub>3</sub> is larger than *h*<sub>2</sub> in 614 states, equal in 626 and never smaller: it dominates it. *h*<sub>2</sub> dominates *h*<sub>1</sub> (larger in 1,073 states, never smaller). The heuristic "nearest parcel + spread of the parcels" is larger than *h*<sub>3</sub> in 468 states and never smaller. When your heuristic is larger than *h*<sub>3</sub> in some states and smaller in others, take the maximum of the two.
- **Experiment 3.** With six parcels the time falls together with the number of expansions, from about 28 ms for *h* = 0 to about 8 ms for *h*<sub>3</sub>. All these heuristics are cheap to compute, so the expansions saved turn into time saved. Absolute times depend on the computer.
