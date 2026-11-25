**English** | [Polski](README.pl.md)

# Reference solutions

This directory is public on purpose. It mirrors `modules/`: the solution to the lesson in `modules/02_search/02_bfs_dfs/` is in `solutions/02_search/02_bfs_dfs/`.

## How to use them

1. Try on your own first: read the lesson, fill in `task.py` and run the tests.
2. If you get stuck, use the hints in the lesson's "If you get stuck" section.
3. Only then compare your version with the `task.py` in this directory. Also read `answers.md`, which answers the review questions and lists what a good answer should contain.

A reference solution is only one of several correct implementations. If yours looks different and the tests pass, that is usually fine.

## Material for authors

- `mutants/` holds deliberately broken implementations. Each one matches a common mistake described in the lesson, and the lesson's tests must reject it.
- `alternatives/` holds other correct implementations. The lesson's tests must accept them, so they do not impose a single solution.

You can run a lesson's tests against any of these files, for example the reference solution:

```bash
uv run pytest modules/02_search/02_bfs_dfs --impl=solution
```
