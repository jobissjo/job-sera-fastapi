from app.models.jobs import JobModel

class SavedJobModel(JobModel):
    jobId:str
    userId:str