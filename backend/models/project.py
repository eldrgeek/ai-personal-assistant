from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from core.database import Base
from datetime import datetime
import uuid


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active")  # active, completed, on_hold, cancelled
    priority = Column(String, default="medium")  # high, medium, low
    category = Column(String, nullable=True)  # e.g., "Chi Life", "Family", "Personal Development"
    
    # Date fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    # Flags from initial data
    is_high_priority = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)