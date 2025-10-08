from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.connection import Base
from datetime import datetime

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer,  primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed= Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.utcnow)