from pydantic import BaseModel
from datetime import datetime 
from enum import Enum

class PriorityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TodoBase(BaseModel):
    title: str
    description: str| None = None
    completed: bool = False
    due_date: datetime | None = None
    priority: PriorityLevel = PriorityLevel.MEDIUM
    

class TodoCreate(TodoBase):
    category_ids: list[int] = []

class TodoUpdate(TodoBase):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None
    priority: PriorityLevel | None = None
    category_ids: list[int] | None = None


class Todo(TodoBase):
    id: int
    create_at: datetime
    user_id: int
    delete_at: datetime | None = None
    class Config:
        from_attributes = True

class TodoWithCategories(Todo):
    categories: list["Category"] = []

    class Config:
        from_attributes = True

from schemas.category import Category
TodoWithCategories.model_rebuild()        