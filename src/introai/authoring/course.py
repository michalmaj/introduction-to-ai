"""The course manifest (``course.toml``) and the course map generated from it.

``course.toml`` is the single source of truth for the course structure:
modules, lessons, core and optional lessons, dependencies and readiness.
``COURSE_MAP.md`` and ``COURSE_MAP.pl.md`` are generated from it.
"""

from __future__ import annotations

import argparse
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

KINDS = ("core", "optional")
STATUSES = ("planned", "ready")


@dataclass(frozen=True)
class Lesson:
    id: str
    dir: str
    title: dict[str, str]
    kind: str
    status: str
    requires: tuple[str, ...]


@dataclass(frozen=True)
class Module:
    id: str
    dir: str
    title: dict[str, str]
    lessons: tuple[Lesson, ...]


@dataclass(frozen=True)
class Course:
    modules: tuple[Module, ...]

    def lessons(self) -> list[tuple[Module, Lesson]]:
        return [(module, lesson) for module in self.modules for lesson in module.lessons]


def load_course(path: Path) -> Course:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    modules = []
    for raw in data.get("module", []):
        lessons = tuple(
            Lesson(
                id=lesson["id"],
                dir=lesson["dir"],
                title=dict(lesson["title"]),
                kind=lesson["kind"],
                status=lesson["status"],
                requires=tuple(lesson.get("requires", [])),
            )
            for lesson in raw.get("lesson", [])
        )
        modules.append(Module(raw["id"], raw["dir"], dict(raw["title"]), lessons))
    return Course(tuple(modules))


def _find_cycle(graph: dict[str, tuple[str, ...]]) -> list[str] | None:
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for nxt in graph.get(node, ()):
            if state.get(nxt) == 1:
                return stack[stack.index(nxt) :] + [nxt]
            if nxt in graph and state.get(nxt) is None:
                cycle = visit(nxt)
                if cycle:
                    return cycle
        stack.pop()
        state[node] = 2
        return None

    for node in graph:
        if state.get(node) is None:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def validate(course: Course, repo_root: Path) -> list[str]:
    """Return every problem in the manifest and its relation to the repository."""
    repo_root = Path(repo_root)
    problems: list[str] = []

    module_ids = [module.id for module in course.modules]
    for module_id in sorted({m for m in module_ids if module_ids.count(m) > 1}):
        problems.append(f"duplicate module id {module_id!r}")

    lesson_ids = [lesson.id for _, lesson in course.lessons()]
    for lesson_id in sorted({i for i in lesson_ids if lesson_ids.count(i) > 1}):
        problems.append(f"duplicate lesson id {lesson_id!r}")
    known = set(lesson_ids)

    listed_dirs: set[str] = set()
    for module, lesson in course.lessons():
        if lesson.id.split(".")[0] != module.id.removeprefix("M"):
            problems.append(f"lesson {lesson.id!r} does not belong to module {module.id!r}")
        if lesson.kind not in KINDS:
            problems.append(
                f"lesson {lesson.id!r}: kind must be 'core' or 'optional', got {lesson.kind!r}"
            )
        if lesson.status not in STATUSES:
            problems.append(
                f"lesson {lesson.id!r}: status must be 'planned' or 'ready', got {lesson.status!r}"
            )
        for requirement in lesson.requires:
            if requirement not in known:
                problems.append(f"lesson {lesson.id!r} requires unknown lesson {requirement!r}")
        lesson_dir = f"{module.dir}/{lesson.dir}"
        listed_dirs.add(lesson_dir)
        if lesson.status == "ready":
            for needed in ("", "/README.md", "/README.pl.md"):
                if not (repo_root / f"{lesson_dir}{needed}").exists():
                    problems.append(
                        f"lesson {lesson.id!r} is ready but {lesson_dir}{needed} is missing"
                    )
                    break

    cycle = _find_cycle({lesson.id: lesson.requires for _, lesson in course.lessons()})
    if cycle:
        problems.append("dependency cycle: " + " -> ".join(cycle))

    modules_root = repo_root / "modules"
    if modules_root.is_dir():
        module_dirs = {module.dir for module in course.modules}
        for module_dir in sorted(p for p in modules_root.iterdir() if p.is_dir()):
            if module_dir.name.startswith((".", "__")):
                continue
            rel_module = module_dir.relative_to(repo_root).as_posix()
            if rel_module not in module_dirs:
                problems.append(f"{rel_module}: module directory is not listed in course.toml")
                continue
            for lesson_dir in sorted(p for p in module_dir.iterdir() if p.is_dir()):
                if lesson_dir.name.startswith((".", "__")):
                    continue
                rel_lesson = lesson_dir.relative_to(repo_root).as_posix()
                if rel_lesson not in listed_dirs:
                    problems.append(f"{rel_lesson}: lesson directory is not listed in course.toml")
    return problems


_MAP_TEXT = {
    "pl": {
        "switch": "[English](COURSE_MAP.md) | **Polski**",
        "title": "# Mapa kursu",
        "legend": (
            "Plik generowany z `course.toml` — nie edytuj go ręcznie. "
            "Lekcje **core** tworzą ścieżkę minimalną, lekcje **opcjonalne** ją rozszerzają. "
            "Lekcje „w przygotowaniu” jeszcze nie istnieją."
        ),
        "header": "| ID | Lekcja | Rodzaj | Wymaga | Status |",
        "kind": {"core": "core", "optional": "opcjonalna"},
        "status": {"ready": "gotowa", "planned": "w przygotowaniu"},
        "readme": "README.pl.md",
    },
    "en": {
        "switch": "**English** | [Polski](COURSE_MAP.pl.md)",
        "title": "# Course map",
        "legend": (
            "Generated from `course.toml` — do not edit by hand. "
            "**Core** lessons form the minimal path, **optional** lessons extend it. "
            "Lessons marked “planned” do not exist yet."
        ),
        "header": "| ID | Lesson | Type | Requires | Status |",
        "kind": {"core": "core", "optional": "optional"},
        "status": {"ready": "ready", "planned": "planned"},
        "readme": "README.md",
    },
}


def render_course_map(course: Course, lang: str) -> str:
    """Render ``COURSE_MAP.md`` (``lang="en"``) or ``COURSE_MAP.pl.md`` (``lang="pl"``)."""
    text = _MAP_TEXT[lang]
    lines = [text["switch"], "", text["title"], "", text["legend"]]
    for module in course.modules:
        lines += ["", f"## {module.id} · {module.title[lang]}", "", text["header"]]
        lines.append("|---|---|---|---|---|")
        for lesson in module.lessons:
            title = lesson.title[lang]
            if lesson.status == "ready":
                title = f"[{title}]({module.dir}/{lesson.dir}/{text['readme']})"
            requires = ", ".join(lesson.requires) if lesson.requires else "—"
            lines.append(
                f"| {lesson.id} | {title} | {text['kind'].get(lesson.kind, lesson.kind)} "
                f"| {requires} | {text['status'].get(lesson.status, lesson.status)} |"
            )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or check COURSE_MAP from course.toml.")
    parser.add_argument("--check", action="store_true", help="only report a stale course map")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    course = load_course(args.repo_root / "course.toml")
    problems = validate(course, args.repo_root)
    for lang, name in (("en", "COURSE_MAP.md"), ("pl", "COURSE_MAP.pl.md")):
        path = args.repo_root / name
        rendered = render_course_map(course, lang)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if args.check:
            if current != rendered:
                problems.append(f"{name} is out of date (run tools/course_map.py)")
        elif current != rendered:
            path.write_text(rendered, encoding="utf-8")
    for problem in problems:
        print(problem)
    print(f"course map: {len(course.lessons())} lesson(s), {len(problems)} problem(s)")
    return 1 if problems else 0
