from fastapi import Depends, status,APIRouter, HTTPException
from app.models.job_applications import JobApplicationModel
from app.models.users import ResponseUser
from app.utils.auth import get_current_active_user
router = APIRouter(prefix="/job-application", tags=['job_application'])


@router.post('/')
async def create_job_application(job_application:JobApplicationModel, _current_user :ResponseUser= Depends(get_current_active_user)):
    return job_application