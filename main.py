# CLI (argparse)
import argparse
from pathlib import Path
from typing import List

from models import Task
from storage import (
load_tasks,
save_tasks,
add_task,
update_task,
remove_task,
find_task,
DEFAULT_TASKS_PATH
)
from utils import timeit_print, confirm, safe_print


DEFAULT_PATH = Path("tasks.json")


def cmd_list(path: Path):
    tasks = load_tasks(path)
    if not tasks:
        safe_print("No tasks found.")
        return

    for i, t in enumerate(tasks, start=1):
        status = "[x]" if t.completed else "[ ]"
        safe_print(f"{i:2d}. {status} {t.title} (id: {t.id})")


def cmd_add(path: Path, title: str, description: str = ""):
    task = Task(title, description)
    add_task(task, path)
    safe_print(f"Task added: {task.id} - {task.title}")


def cmd_done(path: Path,  task_id: str):
    task = find_task(task_id, path)
    if not task:
        safe_print("Task not found.")
        return
    task.mark_as_done()
    update_task(task, path)
    safe_print(f"Marked as done: {task.id}")


def cmd_remove(path: Path, task_id:str):
    task = find_task(task_id, path)
    if not task:
        safe_print("Task not found.")
        return
    if confirm(f"Delete task '{task.title}'? (y/N): "):
        removed = remove_task(task_id, path)
        if removed:
            safe_print("Removed.")
        else:
            safe_print("Could not remove (not found).")
    else:
        safe_print("Cancelled.")


def cmd_find(path: Path, task_id: str):
    task = find_task(task_id, path)
    if not task:
        safe_print("Task not found.")
        return
    safe_print("Found:")
    safe_print(task.to_dict())


def cmd_export(path: Path, out_file: Path):
    tasks = load_tasks(path=path)
    if not tasks:
        safe_print("No tasks to export.")
        return
    # We just save JSON copy
    save_tasks(tasks, path=out_file)
    safe_print(f"Exported {len(tasks)} tasks to {out_file}")


@timeit_print
def main(argv: List[str] = None):
    parser = argparse.ArgumentParser(prog="todo", description="Simple To-Do CLI")
    parser.add_argument("--path", "-p", type=Path, default=DEFAULT_PATH, help="Path to tasks JSON file")

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List tasks")

    a = sub.add_parser("add", help="Add a new task")
    a.add_argument("title", help="Task title")
    a.add_argument("-d", "--description", default="", help="Task description")

    d = sub.add_parser("done", help="Mark a task done")
    d.add_argument("id", help="Task id")

    r = sub.add_parser("remove", help="Remove a task")
    r.add_argument("id", help="Task id")

    f = sub.add_parser("find", help="Find a task by id")
    f.add_argument("id", help="Task id")

    e = sub.add_parser("export", help="Export tasks to a file")
    e.add_argument("out", type=Path, help="Output file path")

    args = parser.parse_args(argv)

    path = args.path




