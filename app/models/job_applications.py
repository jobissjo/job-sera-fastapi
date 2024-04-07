from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile


class JobApplicationModel(BaseModel):
    jobId:str
    userId:str
    ableToCommute:bool
    resume:Optional[UploadFile]
    highQualification:str
    experience:int
    coverLetter:str
