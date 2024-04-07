from fastapi import Depends, status,APIRouter, HTTPException
from app.models.job_applications import JobApplicationModel
router = APIRouter(prefix="/job-application", tags=['job_application'])


@router.post('/')
async def create_job_application(job_application:JobApplicationModel):
    return job_application