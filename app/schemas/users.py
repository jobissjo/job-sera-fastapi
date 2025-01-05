from sqlalchemy import Column, Integer, String, Boolean, MetaData, Table
from app.core.database import Base
import uuid
from sqlalchemy.types import CHAR 



class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)
    role = Column(String, default="user")

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column('id', CHAR(36), primary_key=True, 
           default=lambda: str(uuid.uuid4())),
    Column('username', String),
    Column('email', String),
    Column('hashed_password', String),
    Column('active', Boolean, default=True),
    Column('role', String, default="user")
           
)