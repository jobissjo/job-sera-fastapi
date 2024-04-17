from typing import Annotated, Optional
from fastapi import Depends, Form, Response, status,APIRouter, HTTPException, File, UploadFile
from app.models.job_applications import JobApplicationModel, ResponseJobApplication
from app.models.users import ResponseUser
from app.schemas.job_applications import JobApplication
from app.utils.auth import get_current_active_user
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.database import get_db
import os
import uuid

router = APIRouter(prefix="/job-application", tags=['job_application'])


@router.post('/', response_model=ResponseJobApplication)
async def create_job_application(job_application: JobApplicationModel, db: Session = Depends(get_db)):
    job_applicant = JobApplication(name=job_application.name, email=job_application.email,
                   phoneNumber=job_application.phoneNumber, location=job_application.location,
                   jobId=job_application.jobId, userId=job_application.userId,
                   ableToCommute=job_application.ableToCommute, highQualification=job_application.highQualification,
                   experience=job_application.experience,coverLetter=job_application.coverLetter,
                    interviewDates=job_application.interviewDates, resumePath=job_application.resumePath )
    # print(job_application)
    db.add(job_applicant)
    db.commit()
    db.refresh(job_applicant)
    return job_applicant



UPLOAD_DIRECTORY = "assets/resume"  

@router.post('/upload_resume/')
async def upload_resume(resume: UploadFile = File(...)):
    # Ensure that the uploads directory exists, create it if not
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    # Generate a unique filename using UUID
    unique_filename = str(uuid.uuid4()) + "_" + resume.filename

    filename = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    with open(filename, "wb") as file_object:
        file_object.write(resume.file.read())

    return {'filename': unique_filename}


@router.get('/get_resume/')
async def get_resume(file_path: str):
    # Construct the full file path
    full_file_path = os.path.join(UPLOAD_DIRECTORY, file_path)

    # Check if the file exists
    if not os.path.exists(full_file_path):
        raise HTTPException(status_code=404, detail="Resume not found")

    # Open the file and read its contents
    with open(full_file_path, "rb") as file_object:
        resume_content = file_object.read()

    # Return the resume content with appropriate headers
    return Response(content=resume_content, media_type="application/octet-stream")

@router.get('/job/{id}')
async def get_job_application_by_job_id(job_id: str, db:Session = Depends(get_db)):
    job_application = db.query(JobApplication).filter(JobApplication.jobId == job_id).all()
    return job_application


@router.get('/{id}')
async def get_job_application_by_id(id: str, db:Session = Depends(get_db)):
    job_application = db.query(JobApplication).filter(JobApplication.id == id).all()
    return job_application

@router.get('/user/{id}')
async def get_job_application_by_user_id(user_id: str, db:Session = Depends(get_db)):
    job_application = db.query(JobApplication).filter(JobApplication.userId == user_id).all()
    return job_application