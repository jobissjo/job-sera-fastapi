from fastapi import UploadFile, HTTPException
from requests import Session
from app.models.job_applications import JobApplication
from app.schema.job_applications import JobApplicationSchema
import os
import uuid
from sqlalchemy.future import select

UPLOAD_DIRECTORY = "assets/resume"

class JobApplicationService:

    @staticmethod
    async def add_job_application(job_data:JobApplicationSchema, db:Session):
        job_applicant = JobApplication(**job_data.model_dump())
        db.add(job_applicant)
        await db.commit()
        await db.refresh(job_applicant)
        return job_applicant
    
    @staticmethod
    async def upload_resume(resume: UploadFile):
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)
        
        unique_filename = str(uuid.uuid4()) + "_" + resume.filename

        filename = os.path.join(UPLOAD_DIRECTORY, unique_filename)

        with open(filename, "wb") as file_object:
            file_object.write(resume.file.read())

        return {'filename': unique_filename}
    
    @staticmethod
    async def get_job_application_by_id(id: int, db:Session):
        result = await db.execute(select(JobApplication).filter(JobApplication.id == id))
        job_application = result.scalars().first()
        if not job_application:
            raise HTTPException(status_code=404, detail="Job application not found")
        return job_application
    

    @staticmethod
    
    async def get_job_application_by_job_id(job_id: str, db:Session):
        result = db.execute(select(JobApplication).filter(JobApplication.jobId == job_id))
        return result.scalars().all()
    
    @staticmethod
    async def get_job_application_by_user_id(user_id:int, db: Session):
        result = db.execute(select(JobApplication).filter(JobApplication.userId == user_id))
        return result.scalars().all()