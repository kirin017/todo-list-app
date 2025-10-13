from sqlalchemy.orm import Session
from  models.todo import Todo
from schemas.todo import TodoCreate
from schemas.user import UserCreate
from models.user import User
from auth.security import get_password_hash

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Todo).filter(Todo.user_id == user_id).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

def create_todo(db: Session, todo: TodoCreate, user_id: int):
    db_todo = Todo(
        title = todo.title,
        description = todo.description,
        completed = todo.completed,
        user_id=user_id
    )

    db.add(db_todo)

    db.commit()

    db.refresh(db_todo)

    return db_todo

def update_todo(db: Session, todo_id: int, todo: TodoCreate, user_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id==user_id).first()
    
    if db_todo is None:
        return None
    
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo = todo.completed

    db.commit()
    db.refresh(db_todo)

    return db_todo

def delete_todo(db:Session, todo_id, user_id: int):
    db_todo.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

    if db_todo is None:
        return False
    db.delete(db_todo)
    db,commit()

    return True

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

