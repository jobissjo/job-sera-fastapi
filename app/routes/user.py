from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schema.users import ResponseUserFull,  TokenModel, UserModel, CreateUserModel, ResponseUser, VerifyAccount
from app.core.database import get_db
from app.utils.auth import  get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from app.services import UserService


router = APIRouter(tags=["Users"])




@router.post("/users/", response_model=ResponseUser)
async def create_user(user: CreateUserModel, db: Session = Depends(get_db)):
    
    return await UserService.register_user(user, db)


@router.post('/verify-account/', )
async def activate_account(data: VerifyAccount, db: Session = Depends(get_db)):
    response, is_success = await UserService.verify_account(data, db)
    if not is_success:
        raise HTTPException(status_code=400, detail=f"{response}")
    return {"message": response}
    

@router.post("/token", response_model=TokenModel)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await UserService.login_user(form_data, db)



@router.get("/users/me", response_model=ResponseUser)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user



@router.put("/users/me/change-password/")
async def change_password(old_password: str, new_password: str,  db: Session = Depends(get_db), 
                          current_user: ResponseUserFull = Depends(get_current_active_user)):
    message, success = await  UserService.change_password(old_password, new_password, current_user, db)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


