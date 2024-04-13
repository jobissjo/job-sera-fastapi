from sqlalchemy import Column,  String, JSON
from app.utils.database import Base
from sqlalchemy.types import CHAR
import uuid


class SavedJobs(Base):
    __tablename__ = 'saved_jobs'

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    jobTitle = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    description = Column(JSON)
    salary = Column(String)
    shift = Column(String)
    jobType = Column(String)
    experience = Column(String)
    qualifications = Column(JSON)
    responsibilities = Column(JSON)
    userId = Column(String)
    skills= Column(JSON)