from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from core.database import Base
from datetime import datetime
import uuid


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    actual_end_time = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # active, completed, cancelled
    retrospective = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to distractions
    distractions = relationship("SprintDistraction", back_populates="sprint", cascade="all, delete-orphan")


class SprintDistraction(Base):
    __tablename__ = "sprint_distractions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sprint_id = Column(String, ForeignKey("sprints.id"), nullable=False)
    distraction = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    addressed = Column(Boolean, default=False)
    
    # Relationship to sprint
    sprint = relationship("Sprint", back_populates="distractions")