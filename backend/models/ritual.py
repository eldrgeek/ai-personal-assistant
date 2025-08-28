from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from core.database import Base
from datetime import datetime
import uuid


class Ritual(Base):
    __tablename__ = "rituals"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)  # "morning", "evening"
    title = Column(String, nullable=False)  # "Morning Ritual", "Evening Ritual"
    description = Column(Text, nullable=True)
    estimated_duration_minutes = Column(Integer, default=20)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to steps
    steps = relationship("RitualStep", back_populates="ritual", cascade="all, delete-orphan", order_by="RitualStep.order")


class RitualStep(Base):
    __tablename__ = "ritual_steps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ritual_id = Column(String, ForeignKey("rituals.id"), nullable=False)
    step_text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    estimated_minutes = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to ritual
    ritual = relationship("Ritual", back_populates="steps")