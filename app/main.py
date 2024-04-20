from fastapi import  FastAPI, UploadFile, File
from app.utils.database import Base, engine
from typing import Annotated
from app.routes import (user, jobs,user_profile, employer,company, job_applications,
                        saved_jobs, user_notification)
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from pydantic import BaseModel

app = FastAPI()


origins = [
    "https://sample-firebase-project-883bd.web.app",
    "http://localhost:4200"
]

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],  
)
# @app.get('/')
# def hello_world():
#     return {'message':'Your app is successfully deployed'}

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}

# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}

class MyDate(BaseModel):
    date:date
@app.post("/whatever")
async def create_file(date: MyDate):
    return {"file_size": date}

app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(user_profile.router)
app.include_router(employer.router)
app.include_router(company.router)
app.include_router(job_applications.router)
app.include_router(saved_jobs.router)
app.include_router(user_notification.router)

Base.metadata.create_all(bind=engine)


