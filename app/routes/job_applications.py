from typing import Annotated
from fastapi import Depends, Form, status,APIRouter, HTTPException
from app.models.job_applications import JobApplicationModel
from app.models.users import ResponseUser
from app.utils.auth import get_current_active_user
router = APIRouter(prefix="/job-application", tags=['job_application'])


@router.post('/')
async def create_job_application(job_application: Annotated[JobApplicationModel, Form()]):
    return job_application

