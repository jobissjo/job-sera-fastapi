from fastapi import APIRouter, Depends, HTTPException, status
from app.models.jobs import JobModel,CreateJobModel
from sqlalchemy.orm import Session
from app.schemas.jobs import Job, jobs_table
from app.utils.database import get_db, create_table
from sqlalchemy import MetaData, desc
from app.utils.auth import get_current_active_user

router = APIRouter(prefix='/jobs', tags=['jobs'])
metadata = MetaData()



@router.post('/create-job', response_model=JobModel)
async def create_job(job_model:CreateJobModel, db:Session = Depends(get_db), 
                     current_user:Session = Depends(get_current_active_user)):
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    
    if current_user.role != "employer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only employer can create a job")

    job = Job(jobTitle=job_model.jobTitle, company=job_model.company,
              location=job_model.location, description=job_model.description,
              shift=job_model.shift, jobType=job_model.jobType,
              salary=job_model.salary,
              experience=job_model.experience, qualifications= job_model.qualifications,
              additionalDetails = job_model.additionalDetails, employerId=job_model.employerId)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get('/', response_model=list[JobModel])
async def get_jobs(db:Session= Depends(get_db)):
    jobs = db.query(Job).order_by(desc(Job.id)).limit(10).all()
    return jobs


@router.get('/{id}', response_model=JobModel)
async def get_job_by_id( id: str, db : Session= Depends(get_db)):
    
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    filtered_job = db.query(Job).filter(Job.id == id).first()
    if not filtered_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return filtered_job


@router.put('/{id}',response_model=JobModel)
async def update_job(id: str, employer_id:str, job_model:JobModel, db:Session = Depends(get_db)):
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    job = db.query(Job).filter(Job.id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.employerId != employer_id:
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
    job.additionalDetails = job_model.additionalDetails

    db.commit()
    db.refresh(job)

    return job


@router.delete('/{id}')
async def delete_job(id:str, employer_id: str,db:Session= Depends(get_db)):
    if 'jobs' not in metadata.tables:
        create_table(jobs_table)
    job = db.query(Job).filter(Job.id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.employer_id != employer_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don not have access to modify this details")
    
    db.delete(job)
    db.commit()
    db.refresh()

    return {"message", "Job deleted successfully"}

    