from pydantic import BaseModel
from datetime import datetime 


class TodoBase(BaseModel):
    title: string 
    description: string | None = None
    complete: bool = False
    id: int

class Todo(TodoBase):
    pass


class TodoCreate(TodoBase):
    create_at: datetime

    class Config:
        from_attributes = True