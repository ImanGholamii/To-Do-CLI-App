from datetime import datetime
from uuid import uuid4


class Task:
    def __init__(self, title: str, description: str = ""):
        self.id = str(uuid4())
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat(timespec="seconds")
        self.completed = False

    def mark_as_done(self):
        self.completed = True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data: dict):
        title = data.get("title", "")
        description = data.get("description", "")
        new_task = cls(title=title, description=description)
        if "id" in data:
            new_task.id = data["id"]
        if "created_at" in data:
            new_task.created_at = data["created_at"]
        if "completed" in data:
            new_task.completed = data["completed"]
        return new_task

    def __repr__(self):
        return (f"Task(id={self.id!r}, title={self.title!r}, description={self.description!r},"
                f" created_at={self.created_at!r}, completed={self.completed!r}")

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.created_at < other.created_at
