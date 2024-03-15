from pydantic import BaseModel


class JobModel(BaseModel):
    job_title:str
    company:str
    location:str
    description:str
    shift : str
    job_type:str
    experience:str
    qualifications:list[str]
    description:list[str]
    additional_details:list[str]

class CreateJobModel(JobModel):
    employer_id:str