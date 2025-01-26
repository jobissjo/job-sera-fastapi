from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.schema.user_notification import UserNotificationSchema, UserNotificationResponse
from app.core.database import get_db
from app.models.user_notification import UserNotification
from app.utils.auth import get_current_active_user
from app.schema.users import ResponseUser
from app.services import NotificationService

router = APIRouter(prefix='/notification', tags=['Notification'])


@router.post('/', response_model=UserNotificationResponse)
async def create_notification(notification_data:UserNotificationSchema,
                              db: Session = Depends(get_db)):
    return await NotificationService.create_notification(notification_data, db)


@router.get('/', response_model=list[UserNotificationResponse])
async def get_notification_by_job_post(position: str, db: Session = Depends(get_db), 
            current_user: ResponseUser = Depends(get_current_active_user)):
    notifications = NotificationService.notification_by_post(position,current_user.id,db)
    return notifications
    


@router.put('/{id}', response_model=UserNotificationResponse)
async def delete_notification_of_user(id:str, delete_user_id: str = Body(...), db:Session = Depends(get_db),
                                      current_user :ResponseUser = Depends(get_current_active_user)):
    
    return await NotificationService.delete_user_notifications(id, delete_user_id ,db)

@router.get('/users/{user_id}')
async def get_notification_of_user( user_id: str, db: Session = Depends(get_db), current_user:ResponseUser = Depends(get_current_active_user)):
    
    return await NotificationService.notification_of_user(user_id,db, current_user)


@router.delete('/{notify_id}/users/{user_id}')
async def delete_notification_of_user_by_id(notify_id:str, user_id: str, db: Session = Depends(get_db), current_user:ResponseUser = Depends(get_current_active_user)):
    await NotificationService.delete_notification(notify_id,user_id, db, current_user)
    return {"message", "Your notification has been deleted"}
