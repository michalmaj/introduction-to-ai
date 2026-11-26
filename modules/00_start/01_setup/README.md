**English** | [Polski](README.pl.md)

# Lesson 0.1 — Setup and how to use the course

**Core** · Prerequisites: none. This is the first lesson of the course.

## Learning goals

After this lesson you will be able to:

- run the course on your own computer;
- know what every lesson consists of and how to work through it;
- run a lesson's tests and read their messages;
- find your way around the task world: the warehouse map and the `(row, col)` coordinate convention.

## Setup

### 1. Git and uv

You need two tools:

- **Git** to download the course: [git-scm.com/downloads](https://git-scm.com/downloads);
- **uv** for Python and its libraries: [installation guide](https://docs.astral.sh/uv/getting-started/installation/).

To install uv on macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

To install uv on Windows, in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing, open a **new** terminal window and check that it works: `uv --version`.

### 2. The course

```bash
git clone https://github.com/michalmaj/introduction-to-ai.git
cd introduction-to-ai
uv sync
```

`uv sync` creates a `.venv` environment in the course directory with the right Python version and libraries. uv keeps Python itself and the downloaded packages in its own directory in your user profile, not system-wide, and it does not touch other projects. If you ever want to clean up after the course, besides deleting its directory, clear uv's cache with `uv cache clean` and remove the Python versions uv downloaded with `uv python uninstall 3.12`.

### 3. Running the tests for the first time

From the course's root directory:

```bash
uv run pytest modules/00_start/01_setup
```

Expected result: **the tests fail**. That is how it should be, because this lesson's task is not solved yet. If you see an error such as "command not found" instead of a list of tests, see "If you get stuck".

### 4. Jupyter

```bash
uv run jupyter lab
```

JupyterLab opens in your browser. The experiment notebooks are in the lesson directories, for example `modules/00_start/01_setup/experiments.ipynb`.

## What a lesson is made of

Every lesson is a directory under `modules/`:

| File | What it is for |
|---|---|
| `README.md` | theory, examples and the tasks; read it first |
| `task.py` | the only file you edit: Part A holds answers worked out on paper, Part B holds code |
| `test_task.py` | tests that check `task.py`; you do not need to read or change them |
| `experiments.ipynb` | experiments: first you predict, then you run and compare |

Conceptual lessons, such as 1.1, have no `task.py`, tests or notebook. They consist of text, questions and model answers.

Solutions and answers to the questions live in a separate directory, `solutions/`. They are public, but only look at them after your own attempt.

In lessons with a task, the workflow is always the same:

1. Read `README.md`.
2. Fill in `task.py`.
3. Run the lesson's tests and keep fixing until they pass.
4. Do the experiments in the notebook.
5. Answer the review questions, and only then compare yourself with `solutions/`.

**Core** lessons form the minimal path, and **optional** lessons extend it. The full list is in the [course map](../../../COURSE_MAP.md).

## How to read test messages

An example result on an unsolved task:

```text
FAILED modules/00_start/01_setup/test_task.py::test_part_a_start - Failed: Part A: fill in START in task.py
```

In a narrow terminal window this line may be cut off. The full message of every test is further up, in the `FAILURES` section.

- The test's name (`test_part_a_start`) says what is being checked. Tests named `test_part_a_...` check your Part A answers; the others check your code.
- After the dash comes a hint.
- Messages never reveal the correct Part A answer. They only say that it is still missing or wrong.

Passing tests mean your code meets the task's requirements. They do not prove you understand why it works. The experiments and review questions are there for that.

## The task world: the warehouse

Most tasks in the course take place in an automated warehouse. A map is a plain text file, for example `data/maps/small.txt`:

```text
#######
#R..#.#
#.#...#
#...#D#
#######
```

- `#` is an obstacle: a wall or a shelf;
- `.` is free floor;
- `R` is the cell where the robot starts;
- `D` is the dock, which the robot often has to reach.

Later lessons add parcels, marked `P`, and slow zones, marked `~`: free floor that costs more to drive onto (lesson 2.3).

**Coordinates.** A cell is a pair `(row, col)`. Rows are counted from the top, columns from the left, both from zero:

```text
       column
       0123456
row 0  #######
    1  #R..#.#
    2  #.#...#
    3  #...#D#
    4  #######
```

The top-left corner is `(0, 0)`, and the cell `(2, 3)` lies in row 2, column 3. The row always comes first, just like indexing a list of rows in Python: first the row, then the element in that row.

**Directions.** The robot moves in four directions:

- `N` (north): row − 1;
- `E` (east): column + 1;
- `S` (south): row + 1;
- `W` (west): column − 1.

In code you load a map with `WarehouseMap.from_file(...)`. The call `warehouse.is_free(cell)` tells you whether the robot may stand on a cell: whether it lies on the map and is not an obstacle.

## Common mistakes

1. **Swapping row and column.** If you think of a cell as a point `(x, y)` on a chart, it is easy to write the column first. Then every direction rotates by 90°.
2. **Forgetting the obstacles.** A cell next to the robot is not free just because it lies on the map.
3. **Walking off the edge of the map.** A map does not need walls on its edges. A cell outside the map does not exist, so it cannot be a free neighbour. `is_free` checks this for you.

## Task

### Part A: read the map

In `task.py`, write the coordinates of the cells `R` and `D` on the map `data/maps/small.txt`: `START` and `DOCK`, each as a pair `(row, col)`.

### Part B: free neighbours

Implement `free_neighbours(warehouse, cell)`. It returns a list of the free cells next to `cell`, in the order N, E, S, W. Use `warehouse.is_free` to decide whether a cell is free.

### How to check

```bash
uv run pytest modules/00_start/01_setup
```

### Acceptance criteria

- All the lesson's tests pass.
- You can answer the review questions.

## What the tests do not check

- **Understanding of the workflow.** The tests only check your code and answers.
- **Every possible map.** The tests check a few cells of the `small` map and of a small map without border walls.
- **Code style and readability.**

## Experiments

Open [experiments.ipynb](experiments.ipynb). The notebook checks that your environment works, draws the map and shows the free neighbours of the start cell. Before running it, write down which neighbours you expect.

## Review questions

1. Why do the lesson's tests fail right after you download the course, and why is that a good thing?
2. Which cell has the coordinates `(0, 0)`? Why do we write `(row, col)` and not `(x, y)`?
3. How does `uv run pytest modules/00_start/01_setup` differ from a plain `uv run pytest` run from the root directory?

## If you get stuck

<details>
<summary>"uv: command not found" or "uv is not recognized"</summary>

Close the terminal and open a new one, because the installer adds uv to the path only for new windows. If that does not help, go back to the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for your system.

</details>

<details>
<summary>pytest runs the wrong tests or cannot find the lesson</summary>

Make sure you are in the course's root directory (the one with `pyproject.toml`) and that you give the path to the lesson: `uv run pytest modules/00_start/01_setup`. A plain `uv run pytest` runs the course's own tests, not a lesson's.

</details>

<details>
<summary>The tests do not see my changes</summary>

Save `task.py` before running the tests. In the notebook, the first cell turns on automatic reloading, so changes to `task.py` show up without a restart.

</details>

## What to remember

- You set up the course with three commands: `git clone`, `uv sync` and `uv run ...`.
- Every lesson with a task has the same rhythm: README, `task.py`, tests, experiments, review questions, solutions.
- A cell is a pair `(row, col)`, counted from zero from the top-left corner.
- Passing tests are necessary, but they do not prove understanding.

## What next

- After your own attempt, compare yourself with the [solution and answers](../../../solutions/00_start/01_setup/).
- The next lesson: [1.1 What is AI](../../01_agents/01_what_is_ai/README.md).
