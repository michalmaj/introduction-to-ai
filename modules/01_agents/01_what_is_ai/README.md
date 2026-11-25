**English** | [Polski](README.pl.md)

# Lesson 1.1 — What is AI

**Core** · Prerequisites: 0.1 Setup and how to use the course. This is a conceptual lesson without a programming task.

## Learning goals

After this lesson you will be able to:

- explain why "artificial intelligence" has several definitions and how they differ;
- describe the Turing test and its limitations;
- explain what a rational agent is and why this course adopts that view;
- tell narrow AI from general AI, and the symbolic approach from the learning one;
- analyse a real system: what it perceives, what it does and how its success is measured.

## Problem

A spam filter, a chess program, car navigation, a warehouse robot and a customer-service chatbot are all called "artificial intelligence". What do they have in common? Is a thermostat AI too? To answer questions like these we need a shared vocabulary. This lesson introduces it.

## Four views of AI

Definitions of AI differ in two ways. First, whether what matters is **thinking** or **acting**. Second, whether the yardstick is **human beings** or **rationality**, meaning doing what is best for a goal. That gives four views (following Russell and Norvig):

| | Human yardstick | Rational yardstick |
|---|---|---|
| **Thinking** | cognitive modelling: reproduce how humans think | "laws of thought": correct logical reasoning |
| **Acting** | the Turing test: behave like a human | the rational agent: act as well as possible |

- **Thinking humanly.** This goal ties AI to cognitive science. To reach it, you first need to know how the human mind works, which is still largely an open question.
- **Acting humanly.** In 1950 Alan Turing proposed a trial now known as the **Turing test**. A judge has a text conversation with a person and with a machine. If the judge cannot reliably tell which is which, the machine passes. But the test measures resemblance to a person, not effectiveness. It can reward pretending, such as deliberate typos, and a short, smooth conversation does not prove understanding.
- **Thinking rationally.** This is the tradition of logic: deriving true conclusions from true premises. It has two problems. Not all knowledge can be written down in logical form, especially uncertain knowledge. And correct reasoning on its own does not say what to do.
- **Acting rationally.** An agent chooses the actions that, given its knowledge, give the best expected outcome. This view is the most general, because correct reasoning is only one way of acting well. It is also measurable and does not require imitating humans.

This course takes the fourth view: **AI is the design of rational agents.**

## The rational agent

An **agent** is anything that perceives its environment (through sensors) and acts on it (through actuators). A warehouse robot perceives obstacles and parcels, and acts by driving around and picking up parcels. A chess program "perceives" the position on the board and acts by making moves.

A **rational agent**, after every sequence of percepts, chooses the action that, given its knowledge, maximizes the expected **performance measure**: an agreed assessment of how well the agent is doing.

Rationality is not omniscience. What counts is the best choice given what the agent knows at the moment of decision, not how things turned out afterwards. If the robot chose the shortest known route and a trolley unexpectedly blocked the aisle, the robot did not stop being rational. Lesson 1.2 covers the details: percepts, actions, the performance measure and the kinds of environments.

## Narrow and general AI

**Narrow AI** solves a particular task well, such as playing chess, recognizing speech or planning a route. Almost every system in use today is of this kind.

**General AI** would be able to learn and solve a very wide range of tasks, as a person can. It is a research goal and a subject of debate: there is no agreement on its definition, nor on whether or when such a system will exist. Today's large language models handle many different tasks, but their limitations (lesson 9.2) show how far we are from certainty on this question.

## Two traditions: symbolic and learning

- **The symbolic approach:** knowledge and procedures are written down explicitly, as rules, logic or a problem description to search through. Modules 2–5 of this course work this way. The advantage is transparency, because you can explain why the system decided what it did. The disadvantages are brittleness in situations nobody foresaw and the laborious work of writing knowledge down by hand.
- **The learning approach:** behaviour is learned from data, for example by a neural network. Modules 7–9 work this way. The advantage is handling perception and fuzzy patterns. The disadvantages are the need for a lot of data and decisions that are harder to explain.

Many modern systems combine both traditions. For example, AlphaGo (2016) combined neural networks with game-tree search (Monte Carlo Tree Search).

## Common misconceptions

1. **"AI is machine learning."** Machine learning is only part of AI. Search, games, logic and planning are AI techniques that learn nothing.
2. **"A rational system never makes mistakes."** Rationality means the best choice given the available knowledge, not infallibility.
3. **"Passing the Turing test proves understanding."** The test only checks whether the machine can be told apart from a person in conversation.
4. **"The more human-like a system is, the better."** We judge an agent by the performance measure of its task, not by its resemblance to people.

## Task: analysing systems

For each of the five systems, answer questions (a)–(e). Write wherever you like, in a notebook or a text file: what counts is your reasoning.

The systems:

1. An email spam filter.
2. A chess-playing program.
3. A car navigation app.
4. A warehouse robot collecting parcels.
5. A customer-service chatbot for an online shop.

The questions:

- (a) What does the system perceive (what is its input)?
- (b) What actions can it take?
- (c) How would you measure whether it works well (its performance measure)?
- (d) Does it learn from data, follow written rules, or combine both?
- (e) Which of the four views of AI describes it best, and why?

Some answers are debatable, especially (d) and (e). When you compare yourself with the model answers, check the reasoning, not the exact wording.

## How to check

This lesson has no automated tests, because the answers are descriptive. After your own attempt, compare them with the [model answers](../../../solutions/01_agents/01_what_is_ai/answers.md). Each answer comes with an "a good answer contains" checklist you can grade yours against.

## Review questions

1. How does the "acting humanly" view differ from "acting rationally"? Give an example of a system for which the difference matters.
2. Why would passing the Turing test not be a good measure of how well a warehouse robot works?
3. Is a thermostat an agent? Is it rational?
4. Give one advantage and one disadvantage each of the symbolic approach and the learning approach.

## What to remember

- AI can be defined through thinking or acting, with humans or rationality as the yardstick.
- This course sees AI as the design of rational agents: choosing the actions that, given the agent's knowledge, give the best expected outcome.
- Rationality is neither omniscience nor infallibility.
- AI is more than machine learning. The symbolic and learning traditions complement each other.

## What next

- The next lesson: [1.2 Agents and environments](../02_agents_and_environments/README.md).

## References

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, ch. 1.
- A. M. Turing, *Computing Machinery and Intelligence*, Mind 59 (236), 1950, pp. 433–460.
