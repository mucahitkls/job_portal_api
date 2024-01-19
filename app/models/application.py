from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from app.dependencies import Base
from datetime import datetime
import enum


class ApplicationStatus(enum.Enum):
    SUBMITTED = "submitted"
    REVIEWING = "reviewing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    cover_letter = Column(Text)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign keys to reference the job and the applicant
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")

    def __repr__(self):
        return f"<Application(job_id={self.job_id}, applicant_id={self.applicant_id}, status='{self.status.name}')>"
