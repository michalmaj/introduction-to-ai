import textwrap

from introai.authoring.course import load_course, main, render_course_map, validate

SAMPLE = """
[[module]]
id = "M1"
dir = "modules/01_agents"
title = { pl = "Agenci", en = "Agents" }

[[module.lesson]]
id = "1.1"
dir = "01_intro"
title = { pl = "Wstęp", en = "Introduction" }
kind = "core"
status = "ready"
requires = []

[[module.lesson]]
id = "1.2"
dir = "02_more"
title = { pl = "Więcej", en = "More" }
kind = "optional"
status = "planned"
requires = ["1.1"]
"""


def make_repo(tmp_path, toml=SAMPLE, ready_dirs=("modules/01_agents/01_intro",)):
    (tmp_path / "course.toml").write_text(textwrap.dedent(toml))
    for directory in ready_dirs:
        path = tmp_path / directory
        path.mkdir(parents=True, exist_ok=True)
        (path / "README.md").write_text("x")
        (path / "README.pl.md").write_text("x")
    return tmp_path


def problems_for(tmp_path, toml, ready_dirs=("modules/01_agents/01_intro",)):
    repo = make_repo(tmp_path, toml, ready_dirs)
    return validate(load_course(repo / "course.toml"), repo)


def test_valid_sample(tmp_path):
    assert problems_for(tmp_path, SAMPLE) == []


def test_load_course_reads_structure(tmp_path):
    repo = make_repo(tmp_path)
    course = load_course(repo / "course.toml")
    module = course.modules[0]
    assert (module.id, module.dir, module.title["en"]) == ("M1", "modules/01_agents", "Agents")
    assert [lesson.id for lesson in module.lessons] == ["1.1", "1.2"]
    assert module.lessons[1].requires == ("1.1",)


def test_duplicate_lesson_id(tmp_path):
    toml = SAMPLE.replace('id = "1.2"', 'id = "1.1"')
    assert any("duplicate lesson id '1.1'" in p for p in problems_for(tmp_path, toml))


def test_lesson_id_must_match_module(tmp_path):
    toml = SAMPLE.replace('id = "1.2"', 'id = "2.2"').replace('["1.1"]', "[]")
    assert any(
        "'2.2'" in p and "does not belong to module 'M1'" in p for p in problems_for(tmp_path, toml)
    )


def test_bad_kind_and_status(tmp_path):
    toml = SAMPLE.replace('kind = "optional"', 'kind = "extra"').replace(
        'status = "planned"', 'status = "draft"'
    )
    problems = problems_for(tmp_path, toml)
    assert any("kind must be 'core' or 'optional'" in p for p in problems)
    assert any("status must be 'planned' or 'ready'" in p for p in problems)


def test_unknown_requirement(tmp_path):
    toml = SAMPLE.replace('["1.1"]', '["9.9"]')
    assert any("requires unknown lesson '9.9'" in p for p in problems_for(tmp_path, toml))


def test_dependency_cycle(tmp_path):
    toml = SAMPLE.replace("requires = []", 'requires = ["1.2"]')
    assert any(
        "dependency cycle" in p and "1.1" in p and "1.2" in p for p in problems_for(tmp_path, toml)
    )


def test_ready_lesson_needs_directory(tmp_path):
    problems = problems_for(tmp_path, SAMPLE, ready_dirs=())
    assert any("'1.1' is ready" in p and "missing" in p for p in problems)


def test_unlisted_lesson_directory(tmp_path):
    problems = problems_for(
        tmp_path, SAMPLE, ready_dirs=("modules/01_agents/01_intro", "modules/01_agents/09_stray")
    )
    assert any("modules/01_agents/09_stray" in p and "not listed" in p for p in problems)


def test_render_polish_map(tmp_path):
    course = load_course(make_repo(tmp_path) / "course.toml")
    text = render_course_map(course, "pl")
    assert text.startswith("[English](COURSE_MAP.md) | **Polski**\n")
    assert "# Mapa kursu" in text
    assert "## M1 · Agenci" in text
    assert "| ID | Lekcja | Rodzaj | Wymaga | Status |" in text
    assert "| 1.1 | [Wstęp](modules/01_agents/01_intro/README.pl.md) | core | — | gotowa |" in text
    assert "| 1.2 | Więcej | opcjonalna | 1.1 | w przygotowaniu |" in text


def test_render_english_map(tmp_path):
    course = load_course(make_repo(tmp_path) / "course.toml")
    text = render_course_map(course, "en")
    assert text.startswith("**English** | [Polski](COURSE_MAP.pl.md)\n")
    assert "# Course map" in text
    assert "| ID | Lesson | Type | Requires | Status |" in text
    assert (
        "| 1.1 | [Introduction](modules/01_agents/01_intro/README.md) | core | — | ready |" in text
    )
    assert "| 1.2 | More | optional | 1.1 | planned |" in text


def test_main_writes_and_checks(tmp_path, capsys):
    repo = make_repo(tmp_path)
    assert main(["--check", "--repo-root", str(repo)]) == 1
    assert main(["--repo-root", str(repo)]) == 0
    assert (repo / "COURSE_MAP.md").exists() and (repo / "COURSE_MAP.pl.md").exists()
    assert main(["--check", "--repo-root", str(repo)]) == 0
