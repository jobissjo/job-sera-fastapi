from pydantic import BaseModel
from datetime import datetime


class UserNotificationSchema(BaseModel):
    notificationType:str
    title:str
    message:str
    jobId:str
    userId:str = ''
    position:str
    companyName:str
    deleteOrResponded: list[str] = []

class UserNotificationResponse(UserNotificationSchema):
    id:str
    createdDate:datetime 
