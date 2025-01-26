from app.core.database import get_db
from app.models.jobs import Job
from sqlalchemy import desc, select, or_
from app.schema.jobs import CreateJobModel
from app.schema.users import ResponseUser


class JobService:
    @staticmethod
    async def get_jobs(db, page_size=10, page_number=0):
        offset = (page_number - 1) * page_size
        result = await db.execute(select(Job).order_by(
            desc(Job.id)).offset(offset).limit(page_size))
        return result.scalars().all()
    
    @staticmethod
    async def get_job_by_id(job_id:int, db:get_db):
        result = await db.execute(select(Job).filter(Job.id == job_id))
        return result.scalars().first()
    
    @staticmethod
    async def create_job(data:CreateJobModel, db:get_db):
        new_job = Job(**data.model_dump())
        db.add(new_job)
        await db.commit()
        await db.refresh(new_job)
        return new_job
    

    @staticmethod
    async def search_jobs(job_title:str, location:str, 
                          experience:str,db:get_db):
        query = select(Job)

        if job_title:
            query = query.where(Job.jobTitle.like(f'%{job_title}%'))
        if location:
            query = query.where(Job.location.like(f"%{location}%"))
        if experience:
            query = query.where(or_(Job.experience == experience, Job.experience.is_(None)))
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_job(job_id: int, data: CreateJobModel, 
                db: get_db, current_user:ResponseUser):
        job = await JobService.get_job_by_id(job_id, db)
        if not job:
            return "Job not found", None
        if job.employerId != current_user.id:
            return "You don't have access to modify this job", None
        
        for key, value in data.model_dump().items():
            setattr(job, key, value)
        
        await db.commit()
        return None , job
    
    @staticmethod
    async def delete_job(job_id: int, db: get_db, current_user:ResponseUser):
        job = await JobService.get_job_by_id(job_id, db)
        if not job:
            return "Job not found", None
        if job.employerId != current_user.id:
            return "You don't have access to modify this job", None
        
        await db.delete(job)
        await db.commit()
        return None, {"message": "Job Deleted successfully"}
