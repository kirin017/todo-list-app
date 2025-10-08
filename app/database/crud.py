from sqlalchemy.orm import Session
from  models.todo import Todo
from schemas.todo import TodoCreate

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(
        title = todo.title,
        description = todo.description,
        completed = todo.completed
    )

    db.add(db_todo)

    db.commit()

    db.refresh(db_todo)

    return db_todo

def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if db_todo is None:
        return None
    
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo = todo.completed

    db.commit()
    db.refresh(db_todo)

    return db_todo

def delete_todo(db:Session, todo_id):
    db_todo.query(Todo).filter(Todo.id == todo_id).first()

    if db_todo is None:
        return False
    db.delete(db_todo)
    db,commit()

    return True