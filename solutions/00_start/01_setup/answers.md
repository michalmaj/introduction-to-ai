**English** | [Polski](answers.pl.md)

# Lesson 0.1 — answers

Look here only after your own attempt. The tasks are in the [lesson](../../../modules/00_start/01_setup/README.md).

## Part A

`START = (1, 1)` and `DOCK = (3, 5)`. `R` is in row 1 (the second from the top) and column 1. `D` is in row 3 and column 5.

## Review questions

### 1. Why the tests fail right after downloading the course

The `task.py` in a freshly downloaded course is a skeleton: the Part A answers are empty and the functions raise `NotImplementedError`. The tests check your work, so until there is some, they have to fail. If they passed on an empty skeleton, they would check nothing. Going from red to green tests shows that it is your code that meets the requirements.

A good answer contains:

- the fact that `task.py` starts out unfinished;
- the conclusion that tests passing on an empty skeleton would be worthless.

### 2. The coordinates `(0, 0)` and the order `(row, col)`

`(0, 0)` is the top-left corner of the map, the first character of the file's first line. We write `(row, col)` because that is how data arranged in rows is indexed: the map is a list of lines, so we first pick the line (the row) and then the character in it (the column). The `(x, y)` notation from charts uses the opposite order, and its *y* axis points up. Mixing the two conventions rotates the directions.

A good answer contains:

- `(0, 0)` as the top-left corner;
- the reason: rows are indexed first, then characters;
- the remark that `(x, y)` has a different order and a different axis direction.

### 3. `uv run pytest modules/...` versus a plain `uv run pytest`

The command with a path runs the tests of that one lesson, which check your `task.py`. A plain `uv run pytest` in the root directory runs the course's own tests, for its tools and library, not a lesson's. They pass even when no lesson is solved, which is why pytest then prints a reminder of how to check a lesson.

A good answer contains:

- the fact that the path selects a particular lesson's tests;
- the fact that a plain `uv run pytest` checks the course, not your work.
