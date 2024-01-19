from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from app.dependencies import Base
from datetime import datetime
import enum

class EmploymentType(enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=False)
    employment_type = Column(Enum(EmploymentType), default=EmploymentType.FULL_TIME)
    location = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key to reference the HR user who posted the job
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    employer = relationship("User", back_populates="jobs_posted")
    applications = relationship("Application", back_populates="job")

    def __repr__(self):
        return f"<Job(title='{self.title}', employment_type='{self.employment_type.name}', location='{self.location}', is_active={self.is_active})>"
