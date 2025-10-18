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
