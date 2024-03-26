from fastapi import  FastAPI, UploadFile, File
from app.utils.database import Base, engine
from typing import Annotated
from app.routes import user, jobs,user_profile, employer,company

app = FastAPI()

@app.get('/')
def hello_world():
    return {'message':'Your app is successfully deployed'}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(user_profile.router)
app.include_router(employer.router)
app.include_router(company.router)


Base.metadata.create_all(bind=engine)


