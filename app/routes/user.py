from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schema.users import ResponseUserFull,  TokenModel, UserModel, CreateUserModel, ResponseUser
from app.models.users import User, users_table
from app.core.database import get_db, create_table
from app.utils.auth import (get_user, get_email, get_current_active_user,
                            get_password_hash, authenticate_user, create_access_token, verify_password)
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["Users"])
ACCESS_TOKEN_EXPIRE_MINUTES = 30

metadata = MetaData()

@router.post("/users/", response_model=ResponseUser)
async def create_user(user: CreateUserModel, db: Session = Depends(get_db)):
    if "users" not in metadata.tables:
        create_table(users_table)
    # Check if the username is already taken
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    existing_email = get_email(db, user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create the user in the database
    db_user = User(username=user.username, email=user.email,
                            hashed_password=hashed_password, active=user.active, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user



@router.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users/me", response_model=ResponseUser)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user



@router.put("/users/me/change-password/")
async def change_password(old_password: str, new_password: str,  db: Session = Depends(get_db), 
                          current_user: ResponseUserFull = Depends(get_current_active_user)):
    # Verify the old password

    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Verify that the new password is different from the old password
    if old_password == new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the old password")

    # Hash the new password
    hashed_password = get_password_hash(new_password)
    get_user = db.query(User).filter(User.id == current_user.id).first()
    # Update the user's hashed password in the database
    get_user.hashed_password = hashed_password
    db.commit()

    return {"message": "Password updated successfully"}


