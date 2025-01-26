from app.schema.jobs import JobModel

class SavedJobSchema(JobModel):
    jobId:str
    userId:str