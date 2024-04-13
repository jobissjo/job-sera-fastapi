from fastapi import APIRouter, Depends, HTTPException, status
from app.models.jobs import JobModel, ResponseJobModel
from app.models.saved_jobs import SavedJobModel
from sqlalchemy.orm import Session
from app.models.users import ResponseUser
from app.schemas.saved_jobs import SavedJobs
from app.utils.database import get_db, create_table
from sqlalchemy import MetaData, desc
from app.utils.auth import get_current_active_user

router = APIRouter(prefix='/saved_jobs', tags=['Saved Jobs'])
metadata = MetaData()

JOB_NOT_FOUND = "Job not found"

@router.post('/', response_model=JobModel)
async def create_job(job_model:SavedJobModel, db:Session = Depends(get_db), 
                     current_user:ResponseUser = Depends(get_current_active_user)):

    
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized for this request")

    job = SavedJobs(jobTitle=job_model.jobTitle, company=job_model.company,
              location=job_model.location, description=job_model.description,
              shift=job_model.shift, jobType=job_model.jobType,
              salary=job_model.salary,skills=job_model.skills,
              experience=job_model.experience, qualifications= job_model.qualifications,
              responsibilities = job_model.responsibilities, employerId=job_model.userId)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get('/user/{id}', response_model=list[ResponseJobModel])
async def get_jobs(db:Session= Depends(get_db)):
    jobs = db.query(SavedJobs).filter(SavedJobs.id == id).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    return jobs

@router.get('/{id}', response_model=ResponseJobModel)
async def get_job_by_id( id: str, db : Session= Depends(get_db)):
    

    filtered_job = db.query(SavedJobs).filter(SavedJobs.id == id).first()
    if not filtered_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    return filtered_job


@router.delete('/{id}')
async def delete_job(id:str, user_id: str,db:Session= Depends(get_db),
                      current_user:Session = Depends(get_current_active_user)):

    job = db.query(SavedJobs).filter(SavedJobs.id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    if job.userId != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don not have access to modify this details")
    
    db.delete(job)
    db.commit()
    db.refresh()

    return {"message", "Job deleted successfully"}
