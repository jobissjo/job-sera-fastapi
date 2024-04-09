from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile


class JobApplicationModel(BaseModel):
    name:str
    email:str
    phoneNumber:str
    location:str
    jobId:str
    userId:str
    ableToCommute:bool
    resume:Optional[UploadFile]
    highQualification:str
    experience:int
    coverLetter:str
    interviewDates:str
