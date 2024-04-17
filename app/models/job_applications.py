from pydantic import BaseModel,PydanticUserError
from typing import Annotated, Optional
from fastapi import File, UploadFile


class JobApplicationModel(BaseModel):
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

class ResponseJobApplication(JobApplicationModel):
    id:str