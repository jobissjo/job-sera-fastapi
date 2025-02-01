from sqlalchemy import Column,  MetaData, String, JSON, Table
from app.core.database import Base
from sqlalchemy.types import CHAR
import uuid

class Job(Base):
    __tablename__ = 'jobs'

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
    employerId = Column(String)
    skills= Column(JSON)

metadata = MetaData()
jobs_table = Table(
    'jobs',
    metadata,
    Column('id', CHAR(36), primary_key=True, index=True, default=lambda:str (uuid.uuid4())),
    Column('jobTitle', String),
    Column('company', String),
    Column('location', String),
    Column('description', JSON),
    Column('shift', String),
    Column('jobType', String),
    Column('experience', String),
    Column('qualifications', JSON),
    Column('responsibilities', JSON),
    Column('employerId',String),
    Column('skills', JSON)
)