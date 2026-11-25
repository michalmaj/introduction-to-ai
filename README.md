**English** | [Polski](README.pl.md)

# Introduction to Artificial Intelligence

A standalone, self-study introduction to artificial intelligence in Python. The whole course revolves around one question: **how does a machine represent problems, reason, make decisions and solve problems?**

The course covers search, games and constraint satisfaction, nature-inspired algorithms, knowledge and inference, uncertainty, machine learning basics, reinforcement learning and modern AI. Every lesson combines theory, an example traced step by step, a programming task you can check yourself, and experiments. The tasks share one world: an automated warehouse with a delivery robot.

**Start here:** [lesson 0.1 Setup and how to use the course](modules/00_start/01_setup/README.md).

## Who it is for

For people who know Python at the level of object-oriented programming and have taken an introductory statistics course. The course introduces the mathematics it needs, such as logic and probability, on its own.

## Setup

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). It downloads the right Python version by itself.

```bash
git clone https://github.com/michalmaj/introduction-to-ai.git
cd introduction-to-ai
uv sync
```

Open the experiment notebooks with:

```bash
uv run jupyter lab
```

## How to work through a lesson

Every lesson is a directory under `modules/`, for example `modules/02_search/02_bfs_dfs/`.

1. Read the lesson's `README.md`: the theory, an example traced step by step, and the tasks.
2. Fill in `task.py`. It is the only file you edit.
3. Check your work from the repository's root directory:

   ```bash
   uv run pytest modules/02_search/02_bfs_dfs
   ```

4. Open `experiments.ipynb` and run the experiments. Before running each cell, write down what you expect.
5. Only after your own attempt, compare it with the solution in `solutions/`.

Passing tests mean your implementation meets the task's requirements. They do not prove understanding, which is why every lesson also says what its tests do not check.

## Course map

Lessons are either **core**, forming the minimal path, or **optional**, extending it. The full list of modules and lessons, their dependencies and their status is in the [course map](COURSE_MAP.md).

## Solutions

Reference solutions are public and live in [`solutions/`](solutions/README.md). The tasks are there to learn from, not to be graded. You gain the most by comparing a reference solution with your own attempt, not by reading it instead.

## Licenses

- Code: [MIT](LICENSE).
- Educational content, meaning lesson texts, task descriptions, answers and the prose in notebooks: [CC BY-SA 4.0](LICENSE-CONTENT.md).
