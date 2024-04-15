from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_notification import UserNotificationModel, UserNotificationResponse
from app.utils.database import get_db
from app.schemas.user_notification import UserNotification
router = APIRouter(prefix='/notification', tags=['notification'])


@router.post('/', response_model=UserNotificationResponse)
async def create_notification(user_notification_data:UserNotificationModel,
                              db: Session = Depends(get_db)):
    notification = UserNotification(notificationType = user_notification_data.notificationType,
                                    title= user_notification_data.title,
                                    message= user_notification_data.message,
                                    jobId = user_notification_data.jobId,
                                    jobPost = user_notification_data.jobPost,
                                    companyName = user_notification_data.companyName,
                                    deleteOrResponded = user_notification_data.deleteOrResponded)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification