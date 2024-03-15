from sqlalchemy import Column, Integer, MetaData, String, JSON, Table
from typing import List
from app.utils.database import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
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
    Column('id', Integer, primary_key=True),
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