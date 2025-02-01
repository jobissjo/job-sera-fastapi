from sqlalchemy import Column,  String, Boolean, MetaData, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from sqlalchemy.types import CHAR 
from app.models.user_profile import UserProfile


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    active = Column(Boolean, default=True)
    role = Column(String, default="user")
    is_deleted = Column(Boolean, default=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class TempOTP(Base):
    __tablename__ = "temp_otp"
    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(CHAR(36), unique=True, index=True)
    otp = Column(CHAR(6))

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