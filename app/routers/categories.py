from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.category import CategoryCreate, Category
from database import crud
from database.connection import SessionLocal
from models.user import User
from routers.auth import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Category])
def get_all_categories(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    return crud.get_categories(db, user_id=current_user.id)

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    return crud.create_category(db, category=category, user_id=current_user.id)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    success = crud.delete_category(db, category_id=category_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
            ) 
    return None