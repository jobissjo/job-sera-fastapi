from fastapi import APIRouter, Depends, HTTPException, status
from app.schema.jobs import JobModel,CreateJobModel, ResponseJobModel
from sqlalchemy.orm import Session
from app.schema.users import ResponseUser
from app.models.jobs import Job
from app.core.database import get_db
from sqlalchemy import MetaData
from app.utils.auth import  get_current_employer
from typing import Optional
from app.services import JobService

router = APIRouter(prefix='/jobs', tags=['Jobs'])
metadata = MetaData()

JOB_NOT_FOUND = "Job not found"

@router.post('/', response_model=ResponseJobModel)
async def create_job(job_model:CreateJobModel, db:Session = Depends(get_db), 
                     current_employer:ResponseUser = Depends(get_current_employer)):

    
    if current_employer.role != "employer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only employer can create a job")

    return await JobService.create_job(job_model, db)


@router.get('/', response_model=list[ResponseJobModel])
async def get_jobs(db:Session= Depends(get_db),page_size:int=10,
    page_number:int=1):
    
    return await JobService.get_jobs(db,page_size,page_number)

@router.get('/search-result')
async def get_jobs_by_filters(job_title:str,location: Optional[str] = None, 
                              experience: Optional[str] = None, db: Session = Depends(get_db)):
    return await JobService.search_jobs(job_title,location,experience,db)


@router.get('/{id}', response_model=ResponseJobModel)
async def get_job_by_id( id: str, db : Session= Depends(get_db)):
    
    filtered_job = await JobService.get_job_by_id(id, db)
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
    
    error_message, response = await JobService.update_job(id, job_model, db, current_employer)
    if error_message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
    return response


@router.delete('/{id}')
async def delete_job(id:str, db:Session= Depends(get_db),
                      current_employer:ResponseUser = Depends(get_current_employer)):

    error_message, response = await JobService.delete_job(id, db,  current_employer)
    if error_message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
    return response






    