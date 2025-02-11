from pydantic import BaseModel
from datetime import date

class JobApplicationSchema(BaseModel):
    name:str
    email:str
    phoneNumber:str
    location:str
    jobId:str
    userId:str
    ableToCommute:bool
    highQualification:str
    experience:int
    coverLetter:str
    interviewDates:str
    resumePath:str
    role:str
    company:str
    status:str

class ResponseJobApplication(JobApplicationSchema):
    id:str
    appliedOn:date