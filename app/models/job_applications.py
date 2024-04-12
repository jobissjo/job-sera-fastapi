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
    # resume:Optional[UploadFile]
    highQualification:str
    experience:int
    coverLetter:str
    interviewDates:str
