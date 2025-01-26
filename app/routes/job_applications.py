from fastapi import Depends,   APIRouter,  File, UploadFile
from app.schema.job_applications import JobApplicationSchema, ResponseJobApplication
from sqlalchemy.orm import Session
from app.core.database import get_db


from app.services import JobApplicationService
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/job-application", tags=['Job Application'])


@router.post('/', response_model=ResponseJobApplication)
async def create_job_application(job_application: JobApplicationSchema, db: Session = Depends(get_db)):
    
    return await JobApplicationService.add_job_application(job_application, db)



@router.post('/upload_resume/')
async def upload_resume(resume: UploadFile = File(...)):
    
    return await JobApplicationService.upload_resume(resume)



@router.get('/job/{job_id}')
async def get_job_application_by_job_id(job_id: str, db:Session = Depends(get_db)):
   
    return await JobApplicationService.get_job_application_by_id(job_id, db)


@router.get('/{id}')
async def get_job_application_by_id(id: str, db:Session = Depends(get_db)):
    return await JobApplicationService.get_job_application_by_id(id, db)

@router.get('/user/')
async def get_job_application_by_user_id(current_user = Depends(get_current_active_user), db:Session = Depends(get_db)):
    job_application = await JobApplicationService.get_job_application_by_user_id(current_user.id, db)
    return job_application