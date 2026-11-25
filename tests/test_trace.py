import pytest

from introai.trace import Event, TraceLimitExceeded, emit, record


def test_emit_outside_record_is_noop():
    emit("expand", node="A")  # must not raise


def test_record_collects_events_in_order():
    with record() as t:
        emit("a", x=1)
        emit("b", x=2)
    assert [e.kind for e in t.events] == ["a", "b"]
    assert t.events[0].data == {"x": 1}
    assert t.of_kind("b") == [Event("b", {"x": 2})]


def test_limit_raises_when_exceeded():
    with pytest.raises(TraceLimitExceeded), record(limit=2):
        emit("a")
        emit("a")
        emit("a")


def test_limit_allows_exactly_limit_events():
    with record(limit=2) as t:
        emit("a")
        emit("a")
    assert len(t.events) == 2


def test_nested_record_restores_outer():
    with record() as outer:
        emit("a")
        with record() as inner:
            emit("b")
        emit("c")
    assert [e.kind for e in outer.events] == ["a", "c"]
    assert [e.kind for e in inner.events] == ["b"]


def test_recording_stops_after_block():
    with record() as t:
        emit("a")
    emit("b")
    assert [e.kind for e in t.events] == ["a"]


def test_record_can_filter_kinds():
    from introai.trace import wants

    assert not wants("a")
    with record(kinds={"a"}) as t:
        assert wants("a") and not wants("b")
        emit("a", x=1)
        emit("b", x=2)
    assert [e.kind for e in t.events] == ["a"]
    with record() as everything:
        assert wants("anything")
    assert everything.events == []
