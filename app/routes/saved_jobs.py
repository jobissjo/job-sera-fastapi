from fastapi import APIRouter, Depends, HTTPException, status
from app.schema.jobs import ResponseJobModel
from app.schema.saved_jobs import SavedJobModel
from sqlalchemy.orm import Session
from app.schema.users import ResponseUser
from app.models.saved_jobs import SavedJobs
from app.core.database import get_db
from sqlalchemy import MetaData
from app.utils.auth import get_current_active_user

router = APIRouter(prefix='/saved_jobs', tags=['Saved Jobs'])
metadata = MetaData()

JOB_NOT_FOUND = "Job not found"

@router.post('/', response_model=ResponseJobModel)
async def create_job(job_model:SavedJobModel, db:Session = Depends(get_db), 
                     current_user:ResponseUser = Depends(get_current_active_user)):

    
    if current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized for this request")

    job = SavedJobs(jobTitle=job_model.jobTitle, company=job_model.company,
              location=job_model.location, description=job_model.description,
              shift=job_model.shift, jobType=job_model.jobType,
              salary=job_model.salary,skills=job_model.skills,
              experience=job_model.experience, qualifications= job_model.qualifications,
              responsibilities = job_model.responsibilities, userId=job_model.userId)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get('/user/{id}', response_model=list[ResponseJobModel])
async def get_jobs(id: str,db:Session= Depends(get_db),
                   current_user:ResponseUser = Depends(get_current_active_user)):
    jobs = db.query(SavedJobs).filter(SavedJobs.userId == id).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    return jobs

@router.get('/{id}', response_model=ResponseJobModel)
async def get_job_by_id( id: str, db : Session= Depends(get_db),
                        current_user:ResponseUser = Depends(get_current_active_user)):
    

    filtered_job = db.query(SavedJobs).filter(SavedJobs.id == id).first()
    if not filtered_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    return filtered_job


@router.delete('/{id}')
async def delete_job(id:str, db:Session= Depends(get_db),
                      current_user:ResponseUser = Depends(get_current_active_user)):

    job = db.query(SavedJobs).filter(SavedJobs.id == id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
    if job.userId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don not have access to modify this details")
    
    db.delete(job)
    db.commit()

    return {"message", "Job deleted successfully"}
