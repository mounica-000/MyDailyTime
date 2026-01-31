# SQLAlchemy models (DB tables)

from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    label = Column(String, index=True)
    duration_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)