import json
import tempfile
from pathlib import Path
from typing import List, Iterable, Optional

from .models import Task


# Custom Storage Exceptions
class StorageError(Exception):
    """Base class for storage-related errors."""
    pass


class StorageReadError(StorageError):
    """Raised when reading/parsing JSON fails."""
    pass


class StorageWriteError(StorageError):
    """Raised when writing the storage fails."""
    pass


# Default file path
DEFAULT_TASKS_PATH = Path("tasks.json")


# Core Functions
def load_tasks(path: Path = DEFAULT_TASKS_PATH) -> List[Task]:
    """
    Load tasks from a JSON file and return a list of Task instances.
    If the file does not exist, returns an empty list.
    Raises StorageReadError if the file exists but cannot be parsed.
    """
    path = Path(path)  # converting str to Path
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8")  # text:str read_text opens and read content
        data = json.loads(text)  # loads: read str and convert to python obj
        if not isinstance(data, list):
            raise StorageReadError(f"Invalid tasks file format: expected list at top-level, got {type(data)}")
        tasks: List[Task] = []
        for item in data:
            if not isinstance(item, dict):
                continue  # skip invalid entries (not dictionaries)
            tasks.append(Task.from_dict(item))
        return tasks

    except json.JSONDecodeError as e:
        raise StorageReadError(f"Could not parse JSON file {path}: {e}") from e

    except Exception as e:  # Any other unexpected error reading the file
        raise StorageReadError(f"Error reading tasks from {path}: {e}") from e


def save_tasks(tasks: Iterable[Task], path: Path = DEFAULT_TASKS_PATH) -> None:
    """
    Save an iterable of Task objects to the given path as JSON.
    Write is atomic: data is written to a temporary file then moved into place.
    Raises StorageWriteError on failure.
    """
    path = Path(path)

    # prepare serializable task list
    data = [task.to_dict() for task in tasks]

    # ensure target directory exists
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)  # to save file in a dir doesn't exist

    try:
        # write to a temporary file in the same directory for atomic replace
        dir_for_tmp = path.parent or Path(".")
        # delete=False because we want to use file name after closing file
        with tempfile.NamedTemporaryFile("w", dir=str(dir_for_tmp), delete=False, encoding="utf-8") as tmp_f:
            json.dump(data, tmp_f, ensure_ascii=False, indent=2)
            tmp_name = Path(tmp_f.name)
        # replace the target file atomically
        tmp_name.replace(path)
    except Exception as e:
        # try to cleanup temp file if exists
        try:
            if 'tmp_name' in locals() and tmp_name.exists():
                tmp_name.unlink()
        except Exception:
            pass
        raise StorageWriteError(f"Failed to write tasks to {path}: {e}") from e


def add_task(task: Task, path: Path = DEFAULT_TASKS_PATH) -> None:
    loaded_tasks = load_tasks(path)
    loaded_tasks.append(task)
    save_tasks(loaded_tasks, path)


def update_task(updated: Task, path: Path = DEFAULT_TASKS_PATH) -> bool:
    """
    Replace a task with the same id as 'updated'. Returns True if updated, False if not found.
    """
    tasks = load_tasks(path)
    change_flag = False
    for i, t in enumerate(tasks):
        if updated.id == t.id:
            tasks[i] = updated
            change_flag = True
            break
    if change_flag:
        save_tasks(tasks, path)
    return change_flag


def remove_task(task_id: str, path: Path = DEFAULT_TASKS_PATH) -> bool:
    """
    Remove task by id. Returns True if removed, False if not found.
    """
    tasks = load_tasks(path)
    original_tasks_len = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    if original_tasks_len != len(tasks):
        save_tasks(tasks, path)
        return True
    return False


def find_task(task_id: str, path: Path = DEFAULT_TASKS_PATH) -> Optional[Task]:
    tasks = load_tasks(path)
    for t in tasks:
        if t.id == task_id:
            return t
    return None
