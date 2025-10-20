from fastapi import APIRouter, HTTPException, Depends, Query, status
from schemas.todo import TodoBase, Todo, TodoCreate, TodoUpdate, TodoWithCategories, PriorityLevel
from datetime import datetime
from sqlalchemy.orm import Session
from database import crud
from database.connection import SessionLocal
from models.user import User
from routers.auth import get_current_user

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


@router.get("/", response_model=list[TodoWithCategories])
def get_all_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"), 
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    completed: bool | None = Query(None, description="Filter by completion status"),
    priority: PriorityLevel | None = Query(None, description="Filter by priority level"),
    category_id: int | None = Query(None, description="Filter by category ID"),
    search: str | None = Query(None, description="Search in title or description"),
    sort_by: str | None = Query(None, description="Sort by field (e.g., due_date, priority)"),
    include_deleted: bool = Query(False, description="Include deleted todos"),
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    todos = crud.get_todos_advanced(
        db,
        user_id=current_user.id, 
        skip=skip, 
        limit=limit,
        completed=completed,
        priority=priority.value if priority else None,
        category_id=category_id,
        search=search,
        sort_by=sort_by,
        include_deleted=include_deleted
        )
    return todos

@router.get("/overdue", response_model=list[TodoWithCategories])
def get_overdue_todos(
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    todos = crud.get_overdue_todos(db, user_id=current_user.id)
    return todos

@router.get("/{todo_id}", response_model=TodoWithCategories)
def get_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):

    todo = crud.get_todo(db, todo_id=todo_id, user_id=current_user.id)

    if todo is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Todo with id {todo_id} not found"
            )
    return todo

@router.post("/", response_model=TodoWithCategories, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate, 
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)

@router.patch("/{todo_id}", response_model=TodoWithCategories)
def update_todo(
    todo_id: int, 
    todo_update: TodoUpdate, 
    db: Session = Depends(get_db), 
    current_user:User=Depends(get_current_user)
    ):
    update_data = todo_update.model_dump(exclude_unset=True)
    if update_todo is None:
    # If not found, raise 404
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    update_todo = crud.update_todo_advanced(
        db=db,
        todo_id=todo_id,
        todo_update=update_data,
        user_id=current_user.id
    )

    if update_todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return  update_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    success = crud.soft_delete_todo(db, todo_id=todo_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            ) 
    return None

@router.post("/{todo_id}/restore", response_model=TodoWithCategories)
def restore_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    todo = crud.restore_todo(db, todo_id=todo_id, user_id=current_user.id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found or not deleted"
            ) 
    return todo

@router.delete("/{todo_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
def permanently_delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    success = crud.permanently_delete_todo(
        db, 
        todo_id=todo_id, 
        user_id=current_user.id
        )
    print(success)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Todo not found"
            ) 
    return None
