**English** | [Polski](README.pl.md)

# Lesson 1.3 — Agent types and problem formulation

**Core** · Prerequisites: 1.2 Agents and environments.

## Learning goals

After this lesson you will be able to:

- tell apart five types of agents and say what each needs in order to act;
- formulate a task as a search problem: state, actions, transition model, goal test and cost;
- explain what abstraction is and why we use it;
- count the states of a problem and see how fast they multiply;
- implement a problem formulation that a ready-made search algorithm can solve.

## Problem

In lesson 1.2 even the model-based agent wandered around the hall, because it did not know where the parcels were. Now suppose the warehouse system gives the robot the whole map, parcel positions included. Then the robot can plan the whole sequence of actions before it moves.

But before a computer can find such a plan, the task has to be **formulated**: we must say exactly what a state is, what the actions are, what they lead to, and when the goal is reached.

## Five types of agents

| Agent type | What it decides from | Where in the course |
|---|---|---|
| simple reflex | only the current percept and "condition → action" rules | lesson 1.2 |
| model-based | the percept plus an **internal state**: a model of the world built from past percepts | the model-based agent in lesson 1.2 |
| goal-based | a model of the world and a **goal**: it searches for a sequence of actions that reaches the goal | this lesson and module 2 |
| utility-based | a model of the world and a **utility function**: it chooses the best expected outcome, not just "any goal" | module 6 |
| learning | any of the above that also improves from experience | modules 7 and 8 |

A goal-based agent needs two things a reflex agent lacks: a model, meaning knowledge of what happens after each action, and a description of the goal. With them it can predict the effects of actions "in its head" and search for a plan.

## Formulating a problem

A search problem has five components:

| Component | Meaning | In the parcel pickup problem |
|---|---|---|
| initial state | where we start | `(the robot's start cell, the set of all parcels)` |
| actions | what can be done in a state | moves N, E, S, W into free cells; `PICK` when a parcel lies on the robot's cell |
| transition model | where an action leads: `result(state, action)` | a move changes the robot's cell; `PICK` removes the parcel from its cell |
| goal test | whether a state is a goal: `is_goal(state)` | no parcel is left |
| action cost | what a step costs | every action costs 1 |

A **solution** is a sequence of actions leading from the initial state to a goal. An **optimal solution** has the lowest total cost, here the fewest actions.

In the course's code a problem is a class that inherits from `Problem` (from `introai.search`). It has an `initial` attribute and the methods `actions`, `result` and `is_goal`. The cost of 1 per action is inherited. Every search algorithm in module 2 can solve a formulation like this.

## Abstraction

A real robot has an exact position in centimetres, a speed, a battery, a gripper that has to be lowered and raised, and the time each movement takes. Our formulation has none of that: only a grid cell and a set of parcels. That is **abstraction**: deliberately leaving out details that do not matter for the decision.

A good abstraction is:

- **valid:** every plan found in the abstract problem can be carried out in the real world;
- **useful:** the abstract actions are simple enough that carrying them out is not itself a hard problem.

## One world, two representations

| | Lesson 1.2: an agent | Lesson 1.3: a search problem |
|---|---|---|
| What is known | the percept: a parcel here and the free directions | the full state: the robot's cell and all remaining parcels |
| When it decides | at every step, as it goes | the whole sequence is planned in advance |
| What it needs | rules (and possibly memory) | a transition model and a goal test |

It is the same hall with the same parcels, but the representation decides what the agent can do. That is exactly what the course's guiding question is about.

## Trace it by hand

A small map: a corridor with one parcel.

```text
######
#RP.D#
######
```

- **Free cells:** `(1, 1)`, `(1, 2)`, `(1, 3)`, `(1, 4)`, so 4 cells.
- **Sets of parcels:** the parcel is either still there or collected, so there are 2 possible sets: `{(1, 2)}` and `{}`.
- **Number of states:** 4 · 2 = **8**.
- **Initial state:** `((1, 1), frozenset({(1, 2)}))`.
- **Actions at the start:** `["E"]`, because N, S and W lead into walls, and there is no parcel on the start cell.
- **After `E`:** the state `((1, 2), frozenset({(1, 2)}))`. The actions are `["E", "W", "PICK"]`.
- **After `PICK`:** the state `((1, 2), frozenset())`. This is a goal, because no parcel is left.

The optimal plan is `E`, `PICK`: two actions. The dock `D` does not matter here: the goal is to collect the parcels, not to reach the dock.

## How many states there are

In general there are as many states as there are pairs "free cell × subset of parcels":

> number of states = (number of free cells) · 2<sup>(number of parcels)</sup>

The `aisles` map has 155 free cells:

| Number of parcels | Number of states |
|---|---|
| 1 | 310 |
| 5 | 4,960 |
| 10 | 158,720 |
| 20 | 162,529,280 |

Every extra parcel doubles the number of states. Not every state is reachable, but an algorithm looking for the best plan has to visit many of them. This is the **state-space explosion**, which modules 2 and 4 deal with.

## Common mistakes

1. **PICK without a parcel.** `PICK` is possible only on a cell where a parcel lies.
2. **Moving into obstacles.** Actions are only moves into free cells: the robot does not pass through shelves.
3. **The wrong goal test.** The goal is to collect every parcel, not to reach the dock.
4. **A mutable set of parcels.** If the parcels are in a `set` and `result` changes it in place, the previous state changes too. Worse, a `set` cannot be put into another set, so a search algorithm cannot remember the state. Use a `frozenset` and build a new set: `parcels - {cell}`.

The lesson's tests detect each of these mistakes.

## Task

### Part A: the number of states

In `task.py`, set `NUM_STATES` to the number of states of the problem on the map `data/maps/parcels.txt`. Count every combination of a free robot cell and a set of parcels still lying on the floor. Remember that the cells `R`, `D` and `P` are free too.

### Part B: the problem formulation

Implement the class `ParcelPickupProblem(warehouse)`:

- **state:** `(robot_cell, frozenset_of_remaining_parcels)`;
- **`initial`:** `(warehouse.start, frozenset(warehouse.parcels))`. Set it with `super().__init__(...)`;
- **`actions(state)`:** the moves `"N"`, `"E"`, `"S"`, `"W"` that lead to free cells (`warehouse.is_free`), plus `"PICK"` if a parcel lies on the robot's cell; the order of the actions is up to you;
- **`result(state, action)`:** a move changes the robot's cell; `"PICK"` removes the parcel from the robot's cell; the input state stays unchanged;
- **`is_goal(state)`:** true when no parcel is left.

### How to check

```bash
uv run pytest modules/01_agents/03_problem_formulation
```

One of the tests runs the reference BFS on your formulation and compares the plan's length with the optimal one.

### Acceptance criteria

- All the lesson's tests pass.
- You can answer the review questions.

## What the tests do not check

- **Efficiency.** A slow but correct formulation passes the tests.
- **The order of the actions.** The tests compare actions as sets.
- **Behaviour on an illegal action.** The tests do not check what `result` does when it gets an action that `actions` does not list.
- **The quality of your abstraction.** The formulation is given; you think about abstraction in the review questions.

## Experiments

Open [experiments.ipynb](experiments.ipynb). The notebook runs BFS on your formulation for the map with aisles and 1 to 8 parcels, then plots the number of expansions. Before running it, predict how many times BFS's work grows when one parcel is added.

## Review questions

1. How does a goal-based agent differ from a model-based one? Which do we need to plan a route to every parcel before the robot moves?
2. Why does the state hold the set of remaining parcels, and not just the number collected?
3. Why should the set of parcels in a state be a `frozenset` rather than a `set`?
4. Which details of a real warehouse did the formulation leave out? When could that simplification fail?

## If you get stuck

<details>
<summary>Hint 1: the constructor</summary>

`super().__init__(initial_state)` stores the state in the `initial` attribute. Also keep the map, for example in `self.warehouse`, because `actions` needs it.

</details>

<details>
<summary>Hint 2: moves</summary>

The dict `{"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}` turns a move's name into a `(row, col)` offset. A move is possible if the target cell is free.

</details>

<details>
<summary>Hint 3: PICK</summary>

`parcels - {cell}` builds a new `frozenset` without the parcel on the robot's cell and leaves the old one unchanged.

</details>

## What to remember

- Agent types differ in what they know and what they decide from: from rules, through a world model and a goal, to utility and learning.
- A problem formulation is an initial state, actions, a transition model, a goal test and a cost. A solution is a sequence of actions.
- Abstraction leaves out details that do not matter for the decision. It must stay valid and useful.
- The number of states grows exponentially with the number of parcels, that is, with the number of independent elements of the world.

## What next

- After your own attempt, compare yourself with the [solution and answers](../../../solutions/01_agents/03_problem_formulation/).
- Module 2 shows how search algorithms find solutions to problems like this, and what it costs. The list of modules is in the [course map](../../../COURSE_MAP.md).
- Optional: [1.4 A short history of AI](../04_history_of_ai/README.md).

## References

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, ch. 2 and 3.1–3.2.
