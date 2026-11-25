"""Generated Markdown blocks: graph diagrams and step-by-step trace tables.

Lesson pages contain blocks like::

    <!-- generated:trace-table algorithm=bfs example=worked_example lang=pl -->
    (generated content)
    <!-- /generated -->

The content is produced from the reference implementations, so a worked
example in the text can never disagree with the code. ``--check`` fails when a
block is out of date. Trace tables of exercise graphs are refused in lesson
pages (they would give away Part A answers) but allowed in ``solutions/``.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Callable, Sequence
from pathlib import Path

from introai.search import reference
from introai.search.examples import EXAMPLES, EXERCISE_EXAMPLES
from introai.trace import Trace, record

_OPEN = re.compile(r"^<!-- generated:(\S+)((?:\s+[\w-]+=\S+)*)\s*-->\s*$")
_CLOSE = "<!-- /generated -->"
_ALGORITHMS: dict[str, Callable] = {"bfs": reference.bfs, "dfs": reference.dfs}
_LANGS = ("pl", "en")

_TEXT = {
    "pl": {
        "bfs_header": "| Krok | Rozwijany węzeł | Frontier (w kolejności zdejmowania) "
        "| Zbiór osiągniętych (reached) |",
        "dfs_header": "| Krok | Zdjęty węzeł | Wynik | Frontier (w kolejności zdejmowania) "
        "| Rozwinięte |",
        "outcomes": {"expanded": "rozwinięty", "skipped": "pominięty", "goal": "cel"},
        "found": "Cel **{goal}** znaleziony podczas rozwijania **{node}**. Ścieżka: {path}.",
        "initial_goal": "Stan początkowy **{goal}** jest celem. Ścieżka: {path}.",
        "path": "Ścieżka: {path}.",
        "unreachable": "Frontier jest pusty: cel jest nieosiągalny.",
    },
    "en": {
        "bfs_header": "| Step | Expanded node | Frontier (in removal order) | Reached set |",
        "dfs_header": "| Step | Popped node | Outcome | Frontier (in removal order) | Expanded |",
        "outcomes": {"expanded": "expanded", "skipped": "skipped", "goal": "goal"},
        "found": "Goal **{goal}** found while expanding **{node}**. Path: {path}.",
        "initial_goal": "The initial state **{goal}** is a goal. Path: {path}.",
        "path": "Path: {path}.",
        "unreachable": "The frontier is empty: the goal cannot be reached.",
    },
}


class BlockError(ValueError):
    """A block that cannot be rendered (unknown kind, example, parameter...)."""


def _states(items: Sequence) -> str:
    return ", ".join(str(item) for item in items) if items else "—"


def _render_graph(params: dict[str, str]) -> str:
    problem = _example(params)
    arrow = "-->" if problem.directed else "---"
    lines = ["```mermaid", "graph LR"]
    lines += [f"    {a} {arrow} {b}" for a, b in problem.edges()]
    lines.append("```")
    return "\n".join(lines)


def _example(params: dict[str, str]):
    name = params.get("example")
    if name not in EXAMPLES:
        raise BlockError(f"unknown example {name!r}")
    return EXAMPLES[name]()


def _render_trace_table(params: dict[str, str]) -> str:
    algorithm = params.get("algorithm")
    if algorithm not in _ALGORITHMS:
        raise BlockError(f"unknown algorithm {algorithm!r}")
    lang = params.get("lang")
    if lang not in _LANGS:
        raise BlockError(f"unknown lang {lang!r}")
    problem = _example(params)
    with record() as trace:
        result = _ALGORITHMS[algorithm](problem)
    text = _TEXT[lang]
    rows = _bfs_rows(trace) if algorithm == "bfs" else _dfs_rows(trace, text)
    header = text[f"{algorithm}_header"]
    separator = "|" + "---|" * (header.count("|") - 1)
    table = "\n".join([header, separator, *rows])

    if result is None:
        summary = text["unreachable"]
    else:
        path = " → ".join(str(state) for state in result.states())
        steps = trace.of_kind("step")
        if algorithm == "bfs" and steps:
            summary = text["found"].format(
                goal=result.state, node=steps[-1].data["expanded"], path=path
            )
        elif algorithm == "bfs":
            summary = text["initial_goal"].format(goal=result.state, path=path)
        else:
            summary = text["path"].format(path=path)
    return f"{table}\n\n{summary}"


def _bfs_rows(trace: Trace) -> list[str]:
    return [
        f"| {i} | {e.data['expanded']} | {_states(e.data['frontier'])} "
        f"| {_states(e.data['reached'])} |"
        for i, e in enumerate(trace.of_kind("step"), start=1)
    ]


def _dfs_rows(trace: Trace, text: dict) -> list[str]:
    return [
        f"| {i} | {e.data['popped']} | {text['outcomes'][e.data['outcome']]} "
        f"| {_states(e.data['frontier'])} | {_states(e.data['expanded'])} |"
        for i, e in enumerate(trace.of_kind("step"), start=1)
    ]


_RENDERERS: dict[str, Callable[[dict[str, str]], str]] = {
    "graph": _render_graph,
    "trace-table": _render_trace_table,
}


_EPISODE_TEXT = {
    "pl": {
        "header": (
            "| Krok | Pole robota | Percepcja: paczka; wolne kierunki | Akcja | Punkty po kroku |"
        ),
        "yes": "tak",
        "no": "nie",
        "summary": "Po {steps} krokach: zebrane paczki {collected}, wynik {score}.",
    },
    "en": {
        "header": (
            "| Step | Robot's cell | Percept: parcel; free directions | Action "
            "| Score after the step |"
        ),
        "yes": "yes",
        "no": "no",
        "summary": "After {steps} steps: parcels collected {collected}, score {score}.",
    },
}


def _render_episode_table(params: dict[str, str], repo_root: Path | None) -> str:
    """A step-by-step table of a reference agent acting in the parcel world."""
    from introai.agents.reference import ModelBasedAgent, reflex_agent
    from introai.agents.world import ParcelWorld
    from introai.world.warehouse import WarehouseMap

    agents = {"reflex": lambda: reflex_agent, "model_based": ModelBasedAgent}
    if params.get("agent") not in agents:
        raise BlockError(f"unknown agent {params.get('agent')!r}")
    if params.get("lang") not in _EPISODE_TEXT:
        raise BlockError(f"unknown lang {params.get('lang')!r}")
    if repo_root is None:
        raise BlockError("episode tables need the repository root to load maps")
    map_path = Path(repo_root) / "data" / "maps" / f"{params.get('map')}.txt"
    if not map_path.exists():
        raise BlockError(f"unknown map {params.get('map')!r}")
    try:
        steps = int(params.get("steps", ""))
    except ValueError:
        raise BlockError(f"steps must be a number, got {params.get('steps')!r}") from None

    text = _EPISODE_TEXT[params["lang"]]
    agent = agents[params["agent"]]()
    world = ParcelWorld(WarehouseMap.from_file(map_path))
    rows = []
    for step in range(1, steps + 1):
        if world.done:
            break
        cell = world.robot
        percept = world.percept()
        action = agent(percept)
        world.step(action)
        seen = text["yes"] if percept.parcel_here else text["no"]
        rows.append(
            f"| {step} | ({cell[0]}, {cell[1]}) | {seen}; {_states(percept.free)} "
            f"| {action} | {world.score} |"
        )
    separator = "|" + "---|" * (text["header"].count("|") - 1)
    summary = text["summary"].format(
        steps=world.steps, collected=world.collected, score=world.score
    )
    return "\n".join([text["header"], separator, *rows]) + "\n\n" + summary


def render_block(kind: str, params: dict[str, str], repo_root: Path | None = None) -> str:
    """Render the content of one generated block."""
    if kind == "episode-table":
        return _render_episode_table(params, repo_root)
    if kind not in _RENDERERS:
        raise BlockError(f"unknown generated block kind {kind!r}")
    return _RENDERERS[kind](params)


def process_file(path: Path, *, check: bool, repo_root: Path) -> list[str]:
    """Regenerate (or, with ``check``, verify) every block in one Markdown file."""
    path = Path(path)
    rel = path.relative_to(repo_root).as_posix()
    in_lessons = rel.startswith("modules/")
    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    problems: list[str] = []
    i = 0
    while i < len(lines):
        match = _OPEN.match(lines[i])
        if not match:
            output.append(lines[i])
            i += 1
            continue
        start = i
        end = next((j for j in range(i + 1, len(lines)) if lines[j].strip() == _CLOSE), None)
        if end is None:
            problems.append(f"{rel}: generated block at line {start + 1} is not closed")
            output.extend(lines[i:])
            break
        kind = match.group(1)
        params = dict(item.split("=", 1) for item in match.group(2).split())
        current = "\n".join(lines[start + 1 : end])
        try:
            if kind == "trace-table" and in_lessons and params.get("example") in EXERCISE_EXAMPLES:
                raise BlockError(
                    f"trace tables for {params.get('example')!r} would reveal Part A answers"
                )
            rendered = render_block(kind, params, repo_root=Path(repo_root))
        except BlockError as error:
            problems.append(f"{rel}: line {start + 1}: {error}")
            rendered = current
        if check and rendered != current:
            problems.append(
                f"{rel}: generated block at line {start + 1} is out of date "
                "(run tools/generated_blocks.py)"
            )
        output.append(lines[start])
        output.extend(rendered.split("\n") if rendered else [])
        output.append(lines[end])
        i = end + 1

    if not check:
        new_text = "\n".join(output) + "\n"
        if new_text != path.read_text(encoding="utf-8"):
            path.write_text(new_text, encoding="utf-8")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate or check generated Markdown blocks.")
    parser.add_argument("--check", action="store_true", help="only report out-of-date blocks")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    pages = []
    for top in ("modules", "solutions"):
        directory = args.repo_root / top
        if directory.is_dir():
            pages += sorted(directory.rglob("*.md"))
    problems: list[str] = []
    for page in pages:
        problems += process_file(page, check=args.check, repo_root=args.repo_root)
    for problem in problems:
        print(problem)
    print(f"generated blocks: {len(pages)} page(s), {len(problems)} problem(s)")
    return 1 if problems else 0
