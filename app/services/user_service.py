from fastapi import HTTPException
from app.schema.users import VerifyAccount
from app.models.users import TempOTP, User
from sqlalchemy.future import select

from app.utils.auth import get_email, get_password_hash, get_user, verify_password
from app.utils.auth import authenticate_user, create_access_token
from datetime import timedelta
ACCESS_TOKEN_EXPIRE_MINUTES = 30
class UserService:
    @staticmethod
    async def verify_account(data:VerifyAccount, db):
        result = await db.execute(select(TempOTP).filter(TempOTP.email == data.email))
        otp_instance =  result.scalars().first()
        if otp_instance and otp_instance.otp == data.otp:
            user_result = db.execute(select(User).filter(User.email == data.email))
            user_instance =  user_result.scalars().first()
            if user_instance:
                user_instance.active = True
                await db.commit()
                return "Account verified successfully", True
            return  "Account not verified", False
        return  "Invalid OTP", False
    
    @staticmethod
    async def change_password(old_password, new_password, current_user, db):
       
        if not await verify_password(old_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect old password")

        if old_password == new_password:
            raise HTTPException(status_code=400, detail="New password must be different from the old password")

        
        hashed_password = await get_password_hash(new_password)

        get_user = await UserService.get_user_with_user_id(current_user.id, db)
        
        if get_user:
            get_user.hashed_password = hashed_password
            await db.commit()
            return "Password updated successfully", True
        return "User not found", False
    
    @staticmethod
    async def register_user(user, db):
        # Check if the username is already taken
        existing_user = await get_user(db, user.username)
        if existing_user and existing_user.active:
            raise HTTPException(status_code=400, detail="Username already registered")
        existing_email = await get_email(db, user.email)
        if existing_email and existing_email.active:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = await get_password_hash(user.password)
        
        # Create the user in the database
        db_user = User(username=user.username, email=user.email,
                                hashed_password=hashed_password, active=False, role=user.role)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    async def login_user(form_data, db):
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=401,
                                headers={"WWW-Authenticate": "Bearer"})
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    
    @staticmethod
    async def get_user_with_user_id(user_id, db):
        result = db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    
    