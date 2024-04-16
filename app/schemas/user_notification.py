import uuid
from sqlalchemy import Column,String, JSON, DateTime
from sqlalchemy.types import CHAR
from app.utils.database import Base
from datetime import datetime
import datetime as dt

class UserNotification(Base):
    __tablename__ = 'user_notification'

    id = Column(CHAR(36), primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    notificationType = Column(String)
    title = Column(String)
    message =Column(String) 
    jobId = Column(String)
    position = Column(String)
    companyName = Column(String)
    deleteOrResponded = Column(JSON)
    createdDate = Column(DateTime, default=datetime.now(dt.UTC))

