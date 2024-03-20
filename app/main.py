from fastapi import  FastAPI
from app.utils.database import Base, engine

from app.routes import user, jobs,user_profile, employer

app = FastAPI()


app.include_router(user.router)
app.include_router(jobs.router)
app.include_router(user_profile.router)
app.include_router(employer.router)


@app.get('/')
def hello_world():
    return {'message':'Your app is successfully deployed'}
Base.metadata.create_all(bind=engine)

