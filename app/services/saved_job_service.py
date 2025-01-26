from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.saved_jobs import SavedJobs
from app.schema.saved_jobs import SavedJobSchema
from sqlalchemy.future import select
from utils.constants import JOB_NOT_FOUND


class SavedJobService:

    @staticmethod
    async def create_save_jobs(db:Session, user_id: str, job_data:SavedJobSchema):
        job = SavedJobs(**job_data.model_dump())
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job
    
    @staticmethod
    async def get_user_saved_jobs(user_id: id, db:Session):
        result = await db.execute(select(SavedJobs).filter(SavedJobs.userId == user_id))
        jobs = result.scalars().all()
        if not jobs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
        return jobs
    
    @staticmethod
    async def get_saved_job(db: Session, user_id: str, job_id: int):
        result = await db.execute(select(SavedJobs).filter(SavedJobs.userId == user_id, SavedJobs.jobId == job_id))
        filtered_job = result.scalars().first()
        if not filtered_job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
        return filtered_job
    

    @staticmethod
    async def delete_saved_job(db: Session, user_id: str, job_id: int):
        job = SavedJobService.get_saved_job(db, user_id, job_id)

        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=JOB_NOT_FOUND)
        
        await db.delete(job)
        await db.commit()
        return {"message", "Job deleted successfully"}