from fastapi import APIRouter, HTTPException, Depends
from schemas.todo import TodoBase, Todo, TodoCreate
from datetime import datetime
from sqlalchemy.orm import Session
from database import crud
from database.connection import SessionLocal

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[Todo])
def get_all_todos(skip: int = 0, limit: int=100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@router.get("/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id=todo_id)

    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo

@router.post("/", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    update_todo = crud.update_todo(db=db, todo_id=todo_id, todo=todo_update)
    
    if update_todo is None:
    # If not found, raise 404
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return  update_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo"""
    # Find and remove the todo
    success = crud.delete_todo(db=db, todo_id=todo_id)
    
    if not success:
    # If not found, raise 404
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return {"message": f"Todo {todo_id} deleted successfully"}

