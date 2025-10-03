from fastapi import APIRouter, HTTPException
from schemas.todo import TodoBase, Todo, TodoCreate
from datetime import datetime


router = APIRouter()

todos_db = []
todo_id_counter = 1


@router.get("/todos", response_model=list[Todo])
async def get_todos():
    return todos_db

@router.get("/todos/{todo_id}")
async def get_todo(todo_id):
    for todo in todos_db:
        if todo.id = todo_id:
            return todo
    HTTPException()