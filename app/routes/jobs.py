from fastapi import APIRouter, Depends, HTTPException, status
from app.models.jobs import JobModel,CreateJobModel, ResponseJobModel
from sqlalchemy.orm import Session
from app.models.users import ResponseUser
from app.schemas.jobs import Job, jobs_table
from app.utils.database import get_db, create_table
from sqlalchemy import MetaData, desc
from app.utils.auth import get_current_active_user, get_current_employer
from app.models.users import ResponseUser
from typing import List, Optional

router = APIRouter(prefix='/jobs', tags=['jobs'])
metadata = MetaData()

JOB_NOT_FOUND = "Job not found"

@router.post('/', response_model=ResponseJobModel)
async def create_job(job_model:CreateJobModel, db:Session = Depends(get_db), 
                     current_employer:ResponseUser = Depends(get_current_employer)):
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    
    if current_employer.role != "employer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only employer can create a job")

    job = Job(jobTitle=job_model.jobTitle, company=job_model.company,
              location=job_model.location, description=job_model.description,
              shift=job_model.shift, jobType=job_model.jobType,
              salary=job_model.salary,skills=job_model.skills,
              experience=job_model.experience, qualifications= job_model.qualifications,
              responsibilities = job_model.responsibilities, employerId=job_model.employerId)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get('/', response_model=list[ResponseJobModel])
async def get_jobs(db:Session= Depends(get_db)):
    jobs = db.query(Job).order_by(desc(Job.id)).limit(10).all()
    return jobs

@router.get('/search-result')
def get_jobs_by_filters(job_title:str,location: Optional[str] = None, 
                              experience: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Job)
    print(f"job title: {job_title}, location : {location}, experience : {experience}")
    if job_title:
        query = query.filter(Job.jobTitle.like(f'%{job_title}%'))
    if location:
        query = query.filter(Job.location.like(f"%{location}%") )
    if experience:
        query = query.filter(Job.experience == experience)
    
    return query.all()


@router.get('/{id}', response_model=ResponseJobModel)
async def get_job_by_id( id: str, db : Session= Depends(get_db)):
    
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    filtered_job = db.query(Job).filter(Job.id == id).first()
    if not filtered_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    return filtered_job

@router.get('/employer/{employer_id}')
async def get_job_by_employer_id(employer_id: str, db: Session = Depends(get_db),
                                 _current_employer:ResponseUser = Depends(get_current_employer)):
    filtered_job = db.query(Job).filter(Job.employerId == employer_id).all()
    if not filtered_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job")
    return filtered_job

@router.put('/{id}',response_model=JobModel)
async def update_job(id: str, job_model:JobModel, db:Session = Depends(get_db),
                     current_employer:ResponseUser = Depends(get_current_employer)):
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    job = db.query(Job).filter(Job.id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    if job.employerId != current_employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don not have access to modify this details")
    
    job.jobTitle = job_model.jobTitle
    job.company = job_model.company
    job.location = job_model.location
    job.description = job_model.description
    job.shift = job_model.shift
    job.salary = job_model.salary
    job.jobType = job_model.jobType
    job.experience = job_model.experience
    job.qualifications = job_model.qualifications
    job.responsibilities = job_model.responsibilities

    db.commit()
    db.refresh(job)

    return job


@router.delete('/{id}')
async def delete_job(id:str, db:Session= Depends(get_db),
                      current_employer:ResponseUser = Depends(get_current_employer)):
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    job = db.query(Job).filter(Job.id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    if job.employerId != current_employer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don not have access to modify this details")
    
    db.delete(job)
    db.commit()

    return {"message", "Job deleted successfully"}






    