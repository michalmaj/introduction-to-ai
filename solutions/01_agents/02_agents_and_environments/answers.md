**English** | [Polski](answers.pl.md)

# Lesson 1.2 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/01_agents/02_agents_and_environments/README.md).

## Part A

| Property | Variant 1 | Variant 2 |
|---|---|---|
| observability | `partially`: the robot senses only its cell and its four neighbours | `fully`: the camera shows the whole hall |
| number of agents | `single`: the robot works alone | `multi`: other robots drive around the hall |
| determinism | `deterministic`: every action always has the same effect | `stochastic`: the wheels slip, so a move can fail |
| episodicity | `sequential`: a collected parcel disappears, and the robot's position affects later steps | `sequential`: the same |
| change | `static`: nothing but the robot changes | `dynamic`: other robots drive while ours decides |
| continuity | `discrete`: a grid of cells, steps, six actions | `discrete`: the same |

## Review questions

### 1. Why the reflex agent got stuck

A reflex agent decides only from the current percept and remembers nothing. At the cells `(1, 3)` and `(2, 3)` it gets the same percept every time, so it chooses the same action. As a result it drives back and forth. The world is only partially observable: the percept says neither where the remaining parcels are nor where the robot has already been. The agent lacks an **internal state**, such as a memory of visited cells, or at least some randomness that would break the loop.

A good answer contains:

- the fact that the agent decides only from the current percept and has no memory;
- the observation that in the loop the percepts repeat, so the actions repeat too;
- what is missing: an internal state (lesson 1.3) or randomness.

### 2. The performance measure through the state of the environment

The performance measure should measure what we actually care about: parcels collected and working time. A reward for behaviour ("drives a lot") can be gamed: an agent maximizing such a measure would drive in circles and collect nothing. Besides, the designer often does not know in advance which behaviour is best, so the performance measure should not impose one.

A good answer contains:

- the remark that the performance measure should reflect the goal, not the means;
- an example of behaviour that maximizes a badly chosen measure without reaching the goal.

### 3. What makes variant 2 hardest

The hardest part is the combination of **multiple agents** and **dynamics**. Other robots can take the parcel ours is heading for or block an aisle, and the world changes while our robot deliberates. A plan made from a single camera picture quickly goes out of date, so the robot has to keep observing and changing its plans. Stochasticity adds one more thing: even a good move can fail. In variant 2 full observability is a help, not a difficulty.

A good answer contains:

- a property that makes the task harder, with a concrete consequence for the agent;
- the remark that full observability makes the task easier.

Other well-argued choices, such as stochasticity, are fine too.

### 4. Is a random agent rational

No. A rational agent chooses the action that maximizes the expected performance measure given its knowledge. A random agent ignores its percept: for example it does `PICK` when it knows no parcel lies on its cell and loses a point, although with the same knowledge a better action exists. The experiment shows that on the `parcels` map the random agent did better than the reflex agent. That does not show the random agent is rational, only that our reflex agent is not rational either, since it falls into a loop. Randomness can still be useful in a partially observable world as a way to break out of loops.

A good answer contains:

- a definition of rationality tied to the percept and the performance measure;
- an example of a random agent's action that, given its knowledge, is worse than an available one;
- a comment on the experiment's result: a better score does not mean rationality.

## Experiments

These are the results of the reference implementations. The random agent uses seed 0.

| Map (step limit) | Agent | Score | Parcels | Steps |
|---|---|---|---|---|
| `parcels` (300) | random | −205 | 3 of 3 | 235 |
| `parcels` (300) | reflex | −290 | 1 of 3 | 300 |
| `parcels` (300) | model-based | 11 | 3 of 3 | 19 |
| `aisles` with 4 parcels (1000) | random | −990 | 1 of 4 | 1000 |
| `aisles` with 4 parcels (1000) | reflex | −1000 | 0 of 4 | 1000 |
| `aisles` with 4 parcels (1000) | model-based | −288 | 4 of 4 | 328 |

- **On the `parcels` map** the reflex agent gets stuck after the first parcel. The random agent, although it wastes plenty of steps, collects them all by chance. The model-based agent collects the three parcels in 19 steps, because it heads for rarely visited cells.
- **In the aisles** the random and reflex agents collect almost nothing. The model-based agent collects all four parcels, but its score is still negative: it does not know where the parcels are, so it has to search a large part of the hall. If it knew the whole map, it could plan (lesson 1.3 and module 2).
