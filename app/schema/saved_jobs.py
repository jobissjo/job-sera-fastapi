from app.schema.jobs import JobModel

class SavedJobModel(JobModel):
    jobId:str
    userId:str