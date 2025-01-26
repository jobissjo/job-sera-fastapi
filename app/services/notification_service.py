
from app.models.user_notification import UserNotification
from app.schema.user_notification import UserNotificationSchema
from app.schema.users import ResponseUser
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi import HTTPException


class NotificationService:

    @staticmethod
    async def create_notification(user_notification_data:UserNotificationSchema,
                                db: Session):
        notification = UserNotification(**user_notification_data.model_dump())
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification
    

    @staticmethod
    async def notification_by_post(position:str, user_id:int, db: Session):
        notifications_query = db.query(UserNotification).filter(UserNotification.position.like(f"%{position}%"))

        notifications_query = notifications_query.filter(or_(UserNotification.userId == '', UserNotification.userId.is_(None)))

        notifications = notifications_query.filter(~UserNotification.deleteOrResponded.contains(user_id)).all()
        if not notifications:
            raise HTTPException(status_code=404, detail="No notifications found for the specified job post")

        return notifications
    
    @staticmethod
    async def get_notification_with_id(id:int, user_id:int, db: Session):
        result = db.execute(select(UserNotification).filter(UserNotification.id == id,
                    UserNotification.userId == user_id))
        return result.scalars().first()


    @staticmethod
    async def delete_notification(id:int, user_id:int, db: Session, current_user:ResponseUser):
        notification = await NotificationService.get_notification_with_id(id, user_id, db)

        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        if notification.userId != user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to edit this page")
        
        db.delete(notification)
        await db.commit()
        return {"message": "Your notification has been deleted"}
    
    @staticmethod
    async def notification_of_user(user_id:int, db: Session, current_user:ResponseUser):
        result = await db.execute(select(UserNotification).filter(UserNotification.userId == user_id))
        notifications = result.scalars().all()
        # 
        if not notifications:
            raise HTTPException(status_code=404, detail="Notification not found")
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to edit this page")
        
        return notifications
    

    @staticmethod
    async def delete_user_notifications(db:Session, delete_user_id):
        result =  await db.execute(select(UserNotification).filter(UserNotification.id == id))
        notification = result.scalars().all()

        if not notification:
            raise HTTPException(status_code=404, detail="No notifications found for the id")
        temp_notification = []
        prev_notification = notification.deleteOrResponded
        temp_notification.extend(prev_notification)
        temp_notification.append(delete_user_id)

        notification.deleteOrResponded = temp_notification
        # Update the database
        await db.commit()
        await db.refresh(notification)

        return notification