from sqlalchemy import Column, Integer, MetaData, String, JSON, Table
from app.utils.database import Base
from sqlalchemy.types import CHAR
import uuid

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    job_title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    description = Column(JSON)
    shift = Column(String)
    job_type = Column(String)
    experience = Column(String)
    qualifications = Column(JSON)
    additional_details = Column(JSON)
    employer_id = Column(String)

metadata = MetaData()
jobs_table = Table(
    'jobs',
    metadata,
    Column('id', CHAR(36), primary_key=True, index=True, default=lambda:str (uuid.uuid4())),
    Column('job_title', String),
    Column('company', String),
    Column('location', String),
    Column('description', JSON),
    Column('shift', String),
    Column('job_type', String),
    Column('experience', String),
    Column('qualifications', JSON),
    Column('additional_details', JSON),
    Column('employer_id',String)
)