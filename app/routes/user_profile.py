from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user_profile import UserProfileModel
from app.models.users import UserModel
from sqlalchemy.orm import Session, joinedload
from app.utils.database import get_db
from app.utils.auth import get_current_active_user
from app.utils.user_profile import profile_model_schemas
from app.crud.user_profile import update_user_profile, delete_user_profile
from app.schemas.user_profile import UserProfile

USER_PROFILE_NOT_FOUND = "User profile not found"

router = APIRouter(prefix='/user-profile',tags=["user profile"])


@router.post('/', response_model=UserProfileModel)
async def create_user_profile(user_profile_model:UserProfileModel,
                        current_user:UserModel = Depends(get_current_active_user),
                        db:Session= Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to create a user profile")
    
    user_profile = profile_model_schemas(user_profile_model)
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    return user_profile_model

@router.get('/{profile_id}')
async def get_user_profile(profile_id: str, db: Session = Depends(get_db),
                     _current_user : Session = Depends(get_current_active_user)):
    user_profile = db.query(UserProfile).options(joinedload(UserProfile.personalDetail),
                                                  joinedload(UserProfile.otherPreference),
                                                  joinedload(UserProfile.education),
                                                  joinedload(UserProfile.certifications),
                                                  joinedload(UserProfile.experience),
                                                  joinedload(UserProfile.knownLanguages)).filter(UserProfile.profileId == profile_id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND)
    return user_profile


@router.put('/{profile_id}', response_model=UserProfileModel)
async def update_user_profile_endpoint(profile_id: str, user_profile_model: UserProfileModel,
                                 _current_user: Session = Depends(get_current_active_user),
                                 db: Session = Depends(get_db)):
    user_profile = db.query(UserProfile).options(joinedload(UserProfile.personalDetail),
                                                  joinedload(UserProfile.otherPreference),
                                                  joinedload(UserProfile.education),
                                                  joinedload(UserProfile.certifications),
                                                  joinedload(UserProfile.experience),
                                                  joinedload(UserProfile.knownLanguages)).filter(UserProfile.profileId == profile_id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND)

    updated_user_profile = update_user_profile(db, user_profile, user_profile_model)
    return updated_user_profile


@router.delete('/{profile_id}')
async def delete_user_profile_endpoint(profile_id: str, db: Session = Depends(get_db),
                                 _current_user: Session = Depends(get_current_active_user)):
    user_profile = db.query(UserProfile).options(joinedload(UserProfile.personalDetail),
                                                  joinedload(UserProfile.otherPreference),
                                                  joinedload(UserProfile.education),
                                                  joinedload(UserProfile.certifications),
                                                  joinedload(UserProfile.experience),
                                                  joinedload(UserProfile.knownLanguages)).filter(UserProfile.profileId == profile_id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND)

    delete_user_profile(db, user_profile)

    return {'message': 'user profile is deleted'}
