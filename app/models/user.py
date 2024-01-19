# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_hr = Column(Boolean, default=False)  # Differentiates between regular user and HR
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    jobs_posted = relationship("Job", back_populates="employer")
    applications = relationship("Application", back_populates="applicant")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', is_active={self.is_active}, is_hr={self.is_hr})>"
