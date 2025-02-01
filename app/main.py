from fastapi import  FastAPI, HTTPException
from app.routes import (user, jobs,user_profile, employer,company, job_applications,
                        saved_jobs, user_notification)
from fastapi.middleware.cors import CORSMiddleware
from app.core.exception_handler import global_exception_handler, validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import os

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

app.add_exception_handler(Exception,global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

BASE_DIR = "media"
RESUME_DIR = os.path.join(BASE_DIR, 'resume')
PROFILE_DIR = os.path.join(BASE_DIR, 'profile')

os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(PROFILE_DIR, exist_ok=True)

app.mount('/media/resume', StaticFiles(directory=RESUME_DIR))
app.mount('/media/profile', StaticFiles(directory=PROFILE_DIR))

@app.get('/')
async def welcome_application():
    return {'message': 'Welcome to FastAPI application'}

app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(user_profile.router)
app.include_router(employer.router)
app.include_router(company.router)
app.include_router(job_applications.router)
app.include_router(saved_jobs.router)
app.include_router(user_notification.router)

# Base.metadata.create_all(bind=engine)


