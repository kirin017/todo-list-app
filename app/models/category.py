from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

todo_categories = Table(
    'todo_categories',
    Base.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship("User", back_populates="categories")
    todos = relationship(
        "Todo",
        secondary=todo_categories,
        back_populates="categories"
    )