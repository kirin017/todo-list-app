from sqlalchemy.orm import Session
from  models.todo import Todo
from schemas.todo import TodoCreate
from schemas.user import UserCreate
from schemas.category import CategoryCreate
from models.user import User
from auth.security import get_password_hash
from sqlalchemy import and_, or_
from schemas.todo import PriorityLevel
from models.category import Category
from datetime import date, datetime

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

def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()

def get_category(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()

def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(
        name = category.name,
        user_id = user_id
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category

def delete_category(db: Session, category_id: int, user_id: int):
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()

    if db_category is None:
        return False

    db.delete(db_category)
    db.commit()

    return True


def get_todos_advanced(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
    priority: PriorityLevel | None = None,
    category_id: int | None = None,
    search: str | None = None,
    sort_by: str = "create_at",
    include_deleted: bool = False
):
    query = db.query(Todo).filter(Todo.user_id == user_id)

    if not include_deleted:
        query = query.filter(Todo.delete_at.is_(None))

    if completed is not None:
        query = query.filter(Todo.completed == completed)
    
    if priority:
        query = query.filter(Todo.priority == priority)
    
    if category_id:
        query = query.join(Todo.categories).filter(Category.id == category_id)

    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(Todo.title.ilike(search_term), Todo.description.ilike(search_term)))

    if sort_by == "create_at":
        query = query.order_by(Todo.create_at.desc())
    elif sort_by == "due_date":
        query = query.order_by(Todo.due_date.asc().nulls_last())
    elif sort_by == "priority":
        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }
        query = query.order_by(db.case(priority_order, value=Todo.priority))
    elif sort_by == "title":
        query = query.order_by(Todo.title.asc())

    return query.offset(skip).limit(limit).all()

def get_overdue_todos(db: Session, user_id: int):
    today = date.today()
    return db.query(Todo).filter(
        and_(
        Todo.user_id == user_id,
        Todo.due_date < today,
        Todo.completed == False,
        Todo.delete_at.is_(None)
        )
    ).all()

def create_todo_with_categories(db: Session, todo: TodoCreate, user_id: int):
    db_todo = Todo(
        title = todo.title,
        description = todo.description,
        completed = todo.completed,
        due_date = todo.due_date,
        priority = todo.priority,
        user_id=user_id
    )

    if todo.category_ids:
        categories = db.query(Category).filter(
            and_(
                Category.id.in_(todo.category_ids),
                Category.user_id == user_id
            )
        ).all()
        db_todo.categories = categories

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo

def update_todo_with_categories(db: Session, todo_id: int, todo: dict, user_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id==user_id).first()
    
    if db_todo is None:
        return None
    
    for field, value in todo_update.items():
        if field == "category_ids" and value is not None:
            categories = db.query(Category).filter(
                and_(
                    Category.id.in_(value),
                    Category.user_id == user_id
                )
            ).all()
            db_todo.categories = categories
        elif hasattr(db_todo, field) and value is not None:
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo

def soft_delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id,
        Todo.delete_at.is_(None)
    ).first() 

    if db_todo is None:
        return None
    
    db_todo.delete_at = datetime.utcnow()
    db.commit()
    db.refresh(db_todo)
    return db_todo

def restore_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id,
        Todo.delete_at.is_not(None)
    ).first()

    if db_todo is None:
        return None

    db_todo.delete_at = None
    db.commit()
    db.refresh(db_todo)
    return db_todo

def permanently_delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id,
    ).first()

    if db_todo is None:
        return False

    db.delete(db_todo)
    db.commit()
    return True