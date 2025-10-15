from todo_cli_app.models import Task
from todo_cli_app.storage import load_tasks, add_task, find_task, update_task, save_tasks, remove_task


def test_add_load_find_update_save_tasks(tmp_path):
    path = tmp_path / "tasks.json"
    assert not path.exists()

    t1 = Task("t1_title")
    t2 = Task("t2_title", "d2")
    t3 = Task("t3")

    # save tasks
    save_tasks([t1, t2], path)
    assert path.exists()

    # Add a task
    add_task(t3, path=path)

    # Load a task
    tasks = load_tasks(path)
    assert len(tasks) == 3
    assert tasks[0].title == "t1_title"

    # find_task
    found = find_task(t1.id, path)
    assert found is not None
    assert found.id == t1.id

    # update_task: mark done and update
    t2.mark_as_done()
    assert t2.completed is True
    updated = update_task(t2, path)
    assert updated is True
    reloaded = find_task(t2.id, path)
    assert reloaded is not None and reloaded.completed is True

    # remove_task
    assert len(load_tasks(path)) == 3
    removed = remove_task(t1.id, path)
    assert removed is True
    removed = remove_task(t2.id, path)
    assert removed is True
    removed = remove_task(t3.id, path)
    assert removed is True
    assert load_tasks(path) == []
