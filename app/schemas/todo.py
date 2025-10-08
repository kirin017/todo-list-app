from pydantic import BaseModel
from datetime import datetime 


class TodoBase(BaseModel):
    title: str
    description: str| None = None
    completed: bool = False
    

class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    create_at: datetime
    class Config:
        from_attributes = True