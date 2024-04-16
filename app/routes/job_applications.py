from typing import Annotated
from fastapi import Depends, Form, status,APIRouter, HTTPException, File, UploadFile
from app.models.job_applications import JobApplicationModel
from app.models.users import ResponseUser
from app.utils.auth import get_current_active_user
from pydantic import BaseModel

router = APIRouter(prefix="/job-application", tags=['job_application'])


@router.post('/')
async def create_job_application(job_application: JobApplicationModel):
    return job_application


# @router.post("/submit")
# async def submit_form(name: str = Form(...), email: str = Form(...), contact_num: str = Form(...), location: str = Form(...), resume: UploadFile = File(...)):
#     # Process the form data here (e.g., save to a database)
#     # For now, let's just print the form data
#     resume_bytes = await resume.read()
#     print("Name:", name)
#     print("Email:", email)
#     print("Contact Number:", contact_num)
#     print("Location:", location)
#     print("Resume:", resume.filename)

#     # You can save the resume bytes to a file or database if needed

#     return {"message": "Form submitted successfully"}


class JobApplication(BaseModel):
    name: str
    email: str
    contactNum: str
    location: str
    resume: bytes

@router.post("/submit")
async def submit_form(job_application: JobApplication):
    # Process the form data here (e.g., save to a database)
    # For now, let's just print the form data
    print("Name:", job_application.name)
    print("Email:", job_application.email)
    print("Contact Number:", job_application.contactNum)
    print("Location:", job_application.location)
    # Resume is a bytes object, you can save it to a file or database
    print("Resume:", job_application.resume[:20], "...")

    return {"message": "Form submitted successfully"}