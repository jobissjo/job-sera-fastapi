from pydantic import BaseModel
from datetime import datetime


class UserNotificationModel(BaseModel):
    notificationType:str
    title:str
    message:str
    jobId:str
    position:str
    companyName:str
    deleteOrResponded: list[str] = []

class UserNotificationResponse(UserNotificationModel):
    id:str
    createdDate:datetime 
