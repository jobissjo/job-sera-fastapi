from sqlalchemy import Column, Integer, String, Boolean,Date
from app.core.database import Base
from sqlalchemy.types import CHAR
import uuid
import datetime

class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String)
    phoneNumber = Column(String)
    location = Column(String)
    jobId = Column(String)
    userId = Column(String)
    ableToCommute = Column(Boolean)
    highQualification = Column(String)
    experience = Column(Integer)
    coverLetter = Column(String)
    interviewDates = Column(String)
    resumePath = Column(String)
    role = Column(String)
    company = Column(String)
    status = Column(String)
    appliedOn = Column(Date, default=datetime.date.today)
