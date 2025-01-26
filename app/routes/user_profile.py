from fastapi import APIRouter, Depends, HTTPException, status
from app.schema.user_profile import UserProfileModel
from app.schema.users import UserModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.profile_service import ProfileService
from app.utils.auth import get_current_active_user
from app.utils.constants import USER_PROFILE_NOT_FOUND


router = APIRouter(prefix='/user-profile',tags=["User Profile"])


@router.post('/', response_model=UserProfileModel)
async def create_user_profile(user_profile_data:UserProfileModel,
                        current_user:UserModel = Depends(get_current_active_user),
                        db:Session= Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to create a user profile")
    
    return await ProfileService.create_user_profile(user_profile_data, db)

@router.get('/{profile_id}')
async def get_user_profile(profile_id: str, db: Session = Depends(get_db),
                     _current_user : Session = Depends(get_current_active_user)):
    user_profile = await ProfileService.get_user_profile(profile_id, db)
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND)
    return user_profile


@router.put('/{profile_id}', response_model=UserProfileModel)
async def update_user_profile_endpoint(profile_id: str, user_profile_data: UserProfileModel,
                                 _current_user: Session = Depends(get_current_active_user),
                                 db: Session = Depends(get_db)):
    return ProfileService.update_profile(db,profile_id, user_profile_data)


@router.delete('/{profile_id}')
async def delete_user_profile_endpoint(profile_id: str, db: Session = Depends(get_db),
                                 _current_user: Session = Depends(get_current_active_user)):
    user_profile = await ProfileService.get_user_profile(profile_id, db)
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND)

    await db.delete(user_profile)
    await db.commit()

    return {'message': 'user profile is deleted'}
