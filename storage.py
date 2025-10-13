from pathlib import Path
from typing import List, Iterable, Optional

from models import Task


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
    pass


def save_tasks(tasks: Iterable[Task], path: Path = DEFAULT_TASKS_PATH) -> None:
    """
    Save an iterable of Task objects to the given path as JSON.
    Write is atomic: data is written to a temporary file then moved into place.
    Raises StorageWriteError on failure.
    """
    pass


def add_task(task: Task, path: Path = DEFAULT_TASKS_PATH) -> None:
    pass


def update_task(updated: Task, path: Path = DEFAULT_TASKS_PATH) -> bool:
    """
    Replace a task with the same id as 'updated'. Returns True if updated, False if not found.
    """
    pass


def remove_task(task_id: str, path: Path = DEFAULT_TASKS_PATH) -> bool:
    """
    Remove task by id. Returns True if removed, False if not found.
    """


def find_task(task_id: str, path: Path = DEFAULT_TASKS_PATH) -> Optional[Task]:
    pass
