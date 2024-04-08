from fastapi import Depends, HTTPException,status
from jose import JWTError, jwt
from app.models.users import TokenData, UserModel, ResponseUser
from app.schemas.users import User
from datetime import datetime, timedelta
import datetime as dt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db

from passlib.context import CryptContext


SECRET_KEY = "hdhfh5jdnb7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"



pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_user(db, username: str):
    return db.query(User).filter(User.username == username).first()

def get_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(dt.UTC) + expires_delta
    else:
        expire = datetime.now(dt.UTC) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

async def get_current_active_user(current_user: ResponseUser = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

async def get_current_employer(current_user: ResponseUser = Depends(get_current_active_user)):
    if current_user.role != 'employer':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not allowed for this operation")
    return current_user

