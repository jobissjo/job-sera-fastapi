from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.schema.user_notification import UserNotificationModel, UserNotificationResponse
from app.core.database import get_db
from app.models.user_notification import UserNotification
from app.utils.auth import get_current_active_user
from app.schema.users import ResponseUser

router = APIRouter(prefix='/notification', tags=['Notification'])


@router.post('/', response_model=UserNotificationResponse)
async def create_notification(user_notification_data:UserNotificationModel,
                              db: Session = Depends(get_db)):
    notification = UserNotification(notificationType = user_notification_data.notificationType,
                                    title= user_notification_data.title,
                                    message= user_notification_data.message,
                                    jobId = user_notification_data.jobId,
                                    position = user_notification_data.position,
                                    companyName = user_notification_data.companyName,
                                    deleteOrResponded = user_notification_data.deleteOrResponded,
                                    userId = user_notification_data.userId)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


@router.get('/', response_model=list[UserNotificationResponse])
async def get_notification_by_job_post(position: str, db: Session = Depends(get_db), current_user: ResponseUser = Depends(get_current_active_user)):
    notifications_query = db.query(UserNotification).filter(UserNotification.position.like(f"%{position}%"))

    notifications_query = notifications_query.filter(or_(UserNotification.userId == '', UserNotification.userId.is_(None)))

    notifications = notifications_query.filter(~UserNotification.deleteOrResponded.contains(current_user.id)).all()

    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for the specified job post")

    return notifications


@router.put('/{id}', response_model=UserNotificationResponse)
async def delete_notification_of_user(id:str, delete_user_id: str = Body(...), db:Session = Depends(get_db),
                                      current_user :ResponseUser = Depends(get_current_active_user)):
    notification = db.query(UserNotification).filter(UserNotification.id == id).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found for the id")
    temp_notification = []
    prev_notification = notification.deleteOrResponded
    temp_notification.extend(prev_notification)
    temp_notification.append(delete_user_id)

    notification.deleteOrResponded = temp_notification
    # Update the database
    db.commit()
    db.refresh(notification)

    return notification


@router.get('/users/{user_id}')
async def ger_notification_of_user( user_id: str, db: Session = Depends(get_db), current_user:ResponseUser = Depends(get_current_active_user)):
    # Query the notification
    notifications = db.query(UserNotification).filter(UserNotification.userId == user_id).all()

    if not notifications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if current_user.id != user_id:
        print("i am here")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to edit this page")
    
    return notifications


@router.delete('/{notify_id}/users/{user_id}')
async def delete_notification_of_user_by_id(notify_id:str, user_id: str, db: Session = Depends(get_db), current_user:ResponseUser = Depends(get_current_active_user)):
    # Query the notification
    notification = db.query(UserNotification).filter(UserNotification.id == notify_id,UserNotification.userId == user_id).first()

    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if current_user.id != user_id:
        print("i am here")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to edit this page")
    
    db.delete(notification)
    db.commit()

    return {"message", "Your notification has been deleted"}
