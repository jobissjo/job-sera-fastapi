from pydantic import BaseModel


class JobModel(BaseModel):
    jobTitle:str
    company:str
    location:str
    description:str
    salary:str
    shift : str
    jobType:str
    experience:str
    qualifications:list[str]
    description:list[str]
    additionalDetails:list[str]
    skills:list[str]

class CreateJobModel(JobModel):
    employerId:str