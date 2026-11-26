**English** | [Polski](COURSE_MAP.pl.md)

# Course map

Generated from `course.toml` — do not edit by hand. **Core** lessons form the minimal path, **optional** lessons extend it. Lessons marked “planned” do not exist yet.

## M0 · Getting started

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 0.1 | [Setup and how to use the course](modules/00_start/01_setup/README.md) | core | — | ready |

## M1 · Agents and problem representation

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 1.1 | [What is AI](modules/01_agents/01_what_is_ai/README.md) | core | 0.1 | ready |
| 1.2 | [Agents and environments](modules/01_agents/02_agents_and_environments/README.md) | core | 1.1 | ready |
| 1.3 | [Agent types and problem formulation](modules/01_agents/03_problem_formulation/README.md) | core | 1.2 | ready |
| 1.4 | [A short history of AI](modules/01_agents/04_history_of_ai/README.md) | optional | 1.3 | ready |

## M2 · Search

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 2.1 | [State spaces and search trees](modules/02_search/01_state_space/README.md) | core | 1.3 | ready |
| 2.2 | [BFS and DFS](modules/02_search/02_bfs_dfs/README.md) | core | 2.1 | ready |
| 2.3 | [Uniform-cost search (UCS)](modules/02_search/03_uniform_cost_search/README.md) | core | 2.2 | ready |
| 2.4 | [Heuristics, greedy best-first search and A*](modules/02_search/04_heuristics_and_a_star/README.md) | core | 2.3 | ready |
| 2.5 | Comparing search strategies | core | 2.4 | planned |
| 2.6 | Iterative deepening | optional | 2.5 | planned |
| 2.7 | Designing heuristics | optional | 2.5 | planned |

## M3 · Games and constraint satisfaction

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 3.1 | Games and minimax | core | 2.5 | planned |
| 3.2 | Alpha-beta pruning | core | 3.1 | planned |
| 3.3 | Evaluation functions and depth limits | core | 3.2 | planned |
| 3.4 | Modelling constraint satisfaction problems | core | 2.5 | planned |
| 3.5 | Backtracking with heuristics and forward checking | core | 3.4 | planned |
| 3.6 | Constraint propagation with AC-3 | optional | 3.5 | planned |
| 3.7 | Expectimax: games with chance | optional | 3.3 | planned |
| 3.8 | Monte Carlo tree search | optional | 3.3 | planned |

## M4 · Nature-inspired algorithms

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 4.1 | Local search and simulated annealing | core | 2.5 | planned |
| 4.2 | Genetic algorithms | core | 4.1 | planned |
| 4.3 | Ant colony optimization (ACO) | core | 4.2 | planned |
| 4.4 | Particle swarm optimization (PSO) | optional | 4.3 | planned |
| 4.5 | A genetic algorithm for scheduling | optional | 4.3, 3.5 | planned |
| 4.6 | Boids and emergence | optional | 4.3 | planned |
| 4.7 | A critical look at the metaphor zoo | optional | 4.3 | planned |

## M5 · Knowledge, logic and inference

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 5.1 | Knowledge representation and propositional logic | core | 1.3 | planned |
| 5.2 | Rules and forward chaining | core | 5.1 | planned |
| 5.3 | Backward chaining and an expert system | core | 5.2 | planned |
| 5.4 | Resolution | optional | 5.3 | planned |
| 5.5 | Introduction to first-order logic | optional | 5.3 | planned |

## M6 · Uncertainty and probability

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 6.1 | Conditional probability and Bayes' rule | core | 0.1 | planned |
| 6.2 | Probabilistic inference and Bayesian networks | core | 6.1 | planned |
| 6.3 | Decisions under uncertainty | core | 6.2 | planned |
| 6.4 | Robot localization with a Bayes filter | optional | 6.3 | planned |
| 6.5 | Value of information | optional | 6.3 | planned |
| 6.6 | Naive Bayes classifier | optional | 6.3 | planned |

## M7 · Machine learning and neural network basics

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 7.1 | Learning from data and kNN | core | 5.3 | planned |
| 7.2 | Generalization and overfitting | core | 7.1 | planned |
| 7.3 | The perceptron and a small neural network | core | 7.2 | planned |
| 7.4 | k-means clustering | optional | 7.3 | planned |
| 7.5 | Decision trees | optional | 7.3 | planned |
| 7.6 | Linear regression | optional | 7.3 | planned |
| 7.7 | Neuroevolution | optional | 7.3, 4.2 | planned |

## M8 · Reinforcement learning

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 8.1 | Exploration and exploitation: multi-armed bandits | core | 2.5, 6.3 | planned |
| 8.2 | MDPs and Q-learning | core | 8.1 | planned |
| 8.3 | Value iteration | optional | 8.2 | planned |
| 8.4 | Reward shaping and unintended behaviour | optional | 8.2 | planned |

## M9 · Modern AI and responsibility

| ID | Lesson | Type | Requires | Status |
|---|---|---|---|---|
| 9.1 | Generative and language models | core | 6.3, 7.3 | planned |
| 9.2 | Limits and responsibility | core | 9.1 | planned |
| 9.3 | Tokenization | optional | 9.2 | planned |
| 9.4 | Evaluating AI answers | optional | 9.2 | planned |
