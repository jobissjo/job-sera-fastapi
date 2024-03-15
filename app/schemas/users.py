from sqlalchemy import create_engine, Column, Integer, String, Boolean
from app.utils.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    active = Column(Boolean, default=False)
    role = Column(String, default="user")