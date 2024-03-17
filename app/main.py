from fastapi import  FastAPI
from app.utils.database import Base, engine

from app.routes import user, jobs,user_profile

app = FastAPI()


app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(user_profile.router)

Base.metadata.create_all(bind=engine)

