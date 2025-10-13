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
        new_task = cls(title=data["title"], description=data["description"])
        new_task["id"] = data["id"]
        new_task["created_at"] = data["created_at"]
        new_task["completed"] = data["completed"]
        return new_task
    