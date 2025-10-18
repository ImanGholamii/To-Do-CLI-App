from time import sleep

from ..models import Task


def test_task_creation():
    task = Task("title")
    sleep(1)
    new_task = Task("title")
    assert task.title == "title"
    assert task.description == ""
    assert task.completed is False
    assert isinstance(task.id, str)
    assert isinstance(task.created_at, str)
    assert task < new_task


def test_to_dict_and_from_dict_roundtrip():
    t1 = Task(title="Roundtrip", description="check to_dict/from_dict")
    d = t1.to_dict()
    assert isinstance(d, dict)
    assert d["title"] == "Roundtrip"

    t2 = Task.from_dict(d)
    assert isinstance(t2, Task)
    assert t2.title == t1.title
    assert t2.description == t1.description
    assert t2.id == t1.id
    assert t2.created_at == t1.created_at


def test_eq_and_repr():
    t1 = Task("A")
    t2 = Task("B")
    assert (t1 == t2) is False
    t3 = Task.from_dict(t1.to_dict())
    assert t3 == t1
    r = repr(t1)
    assert "Task" in r and t1.id in r
