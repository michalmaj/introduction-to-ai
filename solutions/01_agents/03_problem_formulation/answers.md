**English** | [Polski](answers.pl.md)

# Lesson 1.3 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/01_agents/03_problem_formulation/README.md).

## Part A

The map `parcels.txt` has 12 free cells: 4 in each of the three middle rows, counting the cells `R`, `D` and `P`. There are 3 parcels, so there are 2³ = 8 sets of remaining parcels. Hence `NUM_STATES = 12 · 8 = 96`.

## Review questions

### 1. A goal-based agent versus a model-based agent

A model-based agent keeps an internal state, so it knows where it has been and what it has seen, but it still reacts step by step. A goal-based agent uses its model of the world to predict the effects of *sequences* of actions and searches for one that reaches the goal. To plan a route to every parcel before the robot moves, we need a goal-based agent. It must have a full model, meaning the map and the parcel positions, and a description of the goal.

A good answer contains:

- the fact that a model-based agent remembers but decides as it goes;
- the fact that a goal-based agent predicts the effects of actions and searches for a plan;
- the conclusion that planning in advance needs a goal-based agent and a full model.

### 2. The set of remaining parcels instead of a count

The state must contain everything needed to predict the effects of actions. A count of collected parcels does not say *which* parcels are still there. So you cannot tell whether `PICK` is possible on a given cell or where to go. Two states with the same number of collected parcels but different parcels left need different plans. The set of parcels tells them apart; the count does not.

A good answer contains:

- the principle that the state must be enough to predict the effects of actions;
- an example of two situations the count cannot tell apart.

### 3. `frozenset` instead of `set`

For two reasons:

- **Immutability.** `result` must build a new state, not change the old one. A search algorithm keeps many states at once, for example in its frontier, so changing one in place would break others.
- **Hashability.** A graph search remembers visited states in a set, and a tuple containing a `set` has no hash, so it cannot be put there.

A good answer contains:

- the argument about immutability and about many states being kept at once;
- the argument about remembering states in a set, which requires hashability.

### 4. What we left out, and when that fails

Among other things, we left out:

- the robot's exact position and speed;
- the time a move or a pick takes;
- the battery;
- other robots;
- the chance that the gripper misses a parcel.

The simplification fails when one of these details changes whether the plan can be carried out. The battery may run out before the plan ends. Another robot may block an aisle, which makes the environment dynamic. `PICK` may fail, which makes it stochastic. Then the plan has to be revised along the way, or the model enriched.

A good answer contains:

- at least two concrete details that were left out;
- a situation in which a plan from the abstract model can no longer be carried out;
- a remedy: replanning along the way, or a richer model.

## Experiments

BFS on the reference formulation. The `aisles` map has 155 free cells. Parcels are added one at a time from the list in the notebook.

| Parcels | States | BFS expansions | Plan length |
|---|---|---|---|
| 1 | 310 | 89 | 14 |
| 2 | 620 | 163 | 19 |
| 3 | 1,240 | 776 | 42 |
| 4 | 2,480 | 1,738 | 51 |
| 5 | 4,960 | 3,519 | 56 |
| 6 | 9,920 | 7,065 | 57 |
| 7 | 19,840 | 16,901 | 66 |
| 8 | 39,680 | 36,140 | 73 |

Your formulation may give slightly different expansion counts if it returns the actions in a different order (for example `PICK` first), but the plan length will be the same.

From three parcels on, the number of expansions roughly doubles with every extra parcel, just like the number of states. Meanwhile the plan length grows slowly. The plan is short, but finding it becomes very expensive. With 20 parcels the state space has over 162 million states. Module 2 shows smarter search (heuristics, A*), and module 4 shows approximate methods.
