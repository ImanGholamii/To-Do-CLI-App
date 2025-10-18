from todo_cli_app.models import Task
from todo_cli_app.storage import save_tasks, add_task, load_tasks
from todo_cli_app.main import cmd_list, cmd_add, cmd_done, cmd_remove
import pytest


def test_list_empty(tmp_path, capsys):
    p = tmp_path / "tasks.json"
    assert not p.exists()
    cmd_list(p)
    captured = capsys.readouterr()
    assert "No tasks found." in captured.out


def test_list_with_tasks(tmp_path, capsys):
    p = tmp_path / "tasks.json"
    t1 = Task("t1_title")
    t2 = Task("t2_title")
    t2.mark_as_done()
    save_tasks([t1, t2], path=p)
    cmd_list(p)
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert any("t1_title" in line and "[ ]" in line for line in out)
    assert any("t2_title" in line and "[x]" in line for line in out)


def test_cmd_add_creates_file_and_task(tmp_path):
    p = tmp_path / "tasks.json"
    cmd_add(p, "new title", "desc")
    tasks = load_tasks(path=p)
    assert len(tasks) == 1
    assert tasks[0].title == "new title"


def test_cmd_done_marks_done(tmp_path):
    p = tmp_path / "tasks.json"
    t = Task("todo")
    save_tasks([t], path=p)
    cmd_done(p, t.id)
    t2 = load_tasks(path=p)[0]
    assert t2.completed is True


def test_cmd_remove_confirm_yes(tmp_path, monkeypatch, capsys):
    p = tmp_path / "tasks.json"
    t = Task("to delete")
    save_tasks([t], path=p)
    # monkeypatch input to 'y'
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")
    cmd_remove(p, t.id)
    captured = capsys.readouterr()
    assert "Removed." in captured.out
    assert load_tasks(path=p) == []


def test_cmd_remove_cancel_no(tmp_path, monkeypatch, capsys):
    p = tmp_path / "tasks.json"
    t = Task("to keep")
    save_tasks([t], path=p)
    # monkeypatch input to 'n'
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")
    cmd_remove(p, t.id)
    captured = capsys.readouterr()
    assert "Cancelled." in captured.out
    assert len(load_tasks(path=p)) == 1
