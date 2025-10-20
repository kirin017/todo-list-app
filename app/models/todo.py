from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime
import enum

class PriorityEnum(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer,  primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed= Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    due_date = Column(Date, nullable=True)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM)
    delete_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="todos")
    categories = relationship(
        "Category",
        secondary="todo_categories",
        back_populates="todos"
    )