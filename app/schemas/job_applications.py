from sqlalchemy import Column, Integer, String, Boolean
from app.utils.database import Base
from sqlalchemy.types import CHAR
import uuid



class JobApplication(Base):
    __tablename__ = 'job_applications'

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, index=True, unique=True)
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
