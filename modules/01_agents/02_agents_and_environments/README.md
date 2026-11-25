**English** | [Polski](README.pl.md)

# Lesson 1.2 — Agents and environments

**Core** · Prerequisites: 1.1 What is AI.

## Learning goals

After this lesson you will be able to:

- describe an agent by its percepts, actions and performance measure;
- tell the agent function from the agent program;
- describe an agent's task with the PEAS scheme;
- classify an environment by six properties;
- implement a simple reflex agent and see in an experiment where its abilities end.

## Problem

A warehouse robot has to collect parcels. It cannot see the whole hall. At every step it only knows whether a parcel lies on its cell and in which of the four directions the way is free. How should such a robot act? And how do we judge whether it acts well?

This lesson introduces the vocabulary for describing situations like this, the agent and its environment, and the first and simplest kind of agent.

## Agent, percept, action

- A **percept** is what the agent receives from its surroundings at a given moment. The **percept sequence** is everything it has received since the start.
- An **action** is what the agent does. By acting, it changes the environment.
- The **agent function** is an abstract description of behaviour: it maps every percept sequence to an action.
- The **agent program** is the concrete code that implements that function on a real machine.

In our world, called the **parcel world** from now on (`introai.agents`):

| Element | Description |
|---|---|
| Percept | `Percept(parcel_here, free)`: whether a parcel lies on the robot's cell, and the free directions in the order N, E, S, W |
| Actions | `N`, `E`, `S`, `W` (drive), `PICK` (pick up a parcel), `WAIT` (wait) |
| Moving into an obstacle | the robot bumps into it and stays where it is |
| End of an episode | all parcels collected, or the step limit reached |

## Performance measure and rationality

The **performance measure** judges how well the agent did its task. In the parcel world:

- every action costs **1 point**;
- every parcel collected earns **10 points**.

The cost of actions means that what counts is not only *whether* the robot collects the parcels, but also *how fast*.

An important principle: we define the performance measure through the **state of the environment**, meaning what we want to achieve, not through how we think the agent ought to behave. If we rewarded "lots of driving", we would get a robot that drives in circles and collects nothing.

As in lesson 1.1, a **rational agent** chooses the action that, given its knowledge, maximizes the expected performance measure. Whether an agent is rational depends on four things:

- the performance measure;
- the knowledge it starts with;
- the available actions;
- the percept sequence so far.

## PEAS

An agent's task is conveniently described by four components, **PEAS** for short:

| | Robot in the parcel world |
|---|---|
| **P**erformance | +10 per parcel, −1 per action |
| **E**nvironment | a hall with shelves, parcels lying on the floor |
| **A**ctuators | wheels (movement in four directions) and a gripper (`PICK`) |
| **S**ensors | a parcel sensor for its own cell, obstacle sensors in four directions |

## Properties of environments

| Property | Question | Possible answers |
|---|---|---|
| observability | Does the percept show the whole state that matters for the decision? | fully (`fully`) or partially (`partially`) |
| number of agents | Are other agents acting in the environment? | single (`single`) or multi (`multi`) |
| determinism | Do the state and the action fully determine the next state? | deterministic (`deterministic`) or stochastic (`stochastic`) |
| episodicity | Are decisions independent episodes, or does the current action affect future situations? | episodic (`episodic`) or sequential (`sequential`) |
| change | Can the environment change while the agent is deliberating? | static (`static`) or dynamic (`dynamic`) |
| continuity | Do states, time and actions take finitely many distinct values? | discrete (`discrete`) or continuous (`continuous`) |

Examples from outside the warehouse:

- Chess without a clock is fully observable, deterministic and discrete, but has two agents.
- Driving a car is partially observable, stochastic, dynamic and continuous.
- Recognizing whether a photo shows a cat is episodic, because each photo is a separate decision.

## Two warehouse variants

These are the two descriptions you need for Part A of the task.

**Variant 1** is the parcel world of this lesson:

- the robot works in the hall alone;
- it senses only whether a parcel lies on its cell and which of the four neighbouring cells are free;
- every action always has the same effect: a move into a free cell always succeeds, a move into an obstacle always ends in a bump;
- nothing except the robot changes;
- the hall is a grid of cells, and the robot acts in steps.

**Variant 2** is the same hall, except that:

- at every step the robot receives a picture from a ceiling camera that shows the whole hall, all parcels and all obstacles;
- other robots drive around the hall at the same time, also collecting parcels;
- the wheels slip: 10% of moves fail and the robot stays where it is;
- the other robots keep moving while our robot decides what to do;
- the hall is still a grid of cells, and the robot still acts in steps.

## The simple reflex agent

The simplest kind of agent is the **simple reflex agent**. It decides only from the current percept, using "condition → action" rules. It remembers nothing.

Our agent's rules, checked in order:

1. If a parcel lies on the cell, do `PICK`.
2. Otherwise, drive in the first free direction in the order N, E, S, W.
3. If no direction is free, do `WAIT`.

## Trace it by hand

The map `data/maps/parcels.txt` contains three parcels `P`:

```text
#######
#R.P#P#
#.#...#
#..P#D#
#######
```

The reflex agent's first steps:

<!-- generated:episode-table agent=reflex map=parcels steps=8 lang=en -->
| Step | Robot's cell | Percept: parcel; free directions | Action | Score after the step |
|---|---|---|---|---|
| 1 | (1, 1) | no; E, S | E | -1 |
| 2 | (1, 2) | no; E, W | E | -2 |
| 3 | (1, 3) | yes; S, W | PICK | 7 |
| 4 | (1, 3) | no; S, W | S | 6 |
| 5 | (2, 3) | no; N, E, S | N | 5 |
| 6 | (1, 3) | no; S, W | S | 4 |
| 7 | (2, 3) | no; N, E, S | N | 3 |
| 8 | (1, 3) | no; S, W | S | 2 |

After 8 steps: parcels collected 1, score 2.
<!-- /generated -->

From step 4 on, the robot drives back and forth between `(1, 3)` and `(2, 3)`. At `(1, 3)` rule 2 chooses S, because N and E are blocked. At `(2, 3)` the same rule chooses N, because N is free and comes first. The agent does not remember that it was just there, so this loop never ends, even though two parcels are still waiting.

## Common mistakes

1. **Ignoring the parcel.** The agent stands on a parcel but drives on, because it checks the directions before the parcel.
2. **The wrong order of directions.** Rule 2 requires the order N, E, S, W. A different order is a different agent.
3. **Driving into walls.** The agent ignores the list of free directions and drives where there is an obstacle.
4. **No rule for being boxed in.** With nowhere to go, the agent still tries to move instead of waiting.

The lesson's tests detect each of these mistakes.

## Task

### Part A: properties of environments

In `task.py`, fill in the dicts `VARIANT_1` and `VARIANT_2`. For each of the six properties, choose one of the two values given in the comment. If something is wrong, the tests report only the number of wrong answers, not which ones. Otherwise, with two options each, they would give the answer away.

### Part B: the reflex agent

Implement `reflex_agent(percept)` following the three rules from the section "The simple reflex agent". The function returns one of the actions `N`, `E`, `S`, `W`, `PICK`, `WAIT`.

### How to check

```bash
uv run pytest modules/01_agents/02_agents_and_environments
```

### Acceptance criteria

- All the lesson's tests pass.
- You can answer the review questions.

## What the tests do not check

- **Whether the rules are good.** The tests only check that the agent follows the given rules, and the experiment shows that these rules are weak.
- **Your reasoning for Part A.** The tests compare values, not your reasoning.
- **Code style and readability.**

## Experiments

Open [experiments.ipynb](experiments.ipynb) and compare three agents:

- a random one;
- the reflex agent (yours);
- the reference model-based agent, which remembers where it has been.

Before running it, write down which agent you think will do best and which worst, first on the `parcels` map and then on the larger map with aisles.

## Review questions

1. Why did the reflex agent get stuck, even though two parcels were still left? What does it lack?
2. Why is it better to define the performance measure through the state of the environment (parcels collected) than through the agent's behaviour (for example "the robot drives a lot")?
3. Which property of variant 2 makes designing an agent hardest, and why?
4. Is a random agent rational in the parcel world?

## If you get stuck

<details>
<summary>Hint 1: the order of the rules</summary>

Check the rules from the top: first the parcel, then the move, last the waiting. In code these are simply three consecutive `if` statements with a `return`.

</details>

<details>
<summary>Hint 2: the first free direction</summary>

`percept.free` is already ordered N, E, S, W. The first free direction is simply the first element of that tuple, if it is not empty.

</details>

## What to remember

- We describe an agent by its percepts, actions and performance measure, and its task with the PEAS scheme.
- The performance measure is defined through the state of the environment, not through the behaviour we would like to see.
- Environments are classified by six properties. They decide what kind of agent we need.
- A simple reflex agent is simple and fast, but it remembers nothing. In a partially observable world it easily falls into loops.

## What next

- After your own attempt, compare yourself with the [solution and answers](../../../solutions/01_agents/02_agents_and_environments/).
- The next lesson, [1.3 Agent types and problem formulation](../03_problem_formulation/README.md), shows agents that remember and plan.

## References

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, ch. 2.
