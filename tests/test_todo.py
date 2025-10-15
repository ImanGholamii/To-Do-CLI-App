import datetime
from time import sleep

import pytest
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



