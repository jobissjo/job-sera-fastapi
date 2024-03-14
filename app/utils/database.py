from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.schemas.users import  Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/job-sera.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()