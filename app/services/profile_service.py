from app.utils.user_profile import profile_model_schemas
from fastapi import HTTPException, status
from sqlalchemy.future import select
from app.models.user_profile import UserProfile
from sqlalchemy.orm import selectinload
from app.utils.constants import USER_PROFILE_NOT_FOUND
from app.crud.user_profile import update_user_profile
from sqlalchemy.orm import Session

class ProfileService:

    @staticmethod
    async def create_user_profile(user_profile_model, db):
        try:
            user_profile = await profile_model_schemas(user_profile_model)
            db.add(user_profile)
            await db.commit()
            await db.refresh(user_profile)
            return user_profile_model
        except Exception as e:
            print(f"Error creating user profile: {e}")
            raise HTTPException(status_code=500, detail="Something goes wrong")
    

    @staticmethod
    async def get_user_profile(profile_id, db):
        user_profile = await db.execute(
            select(UserProfile)
            .options(selectinload(UserProfile.personalDetail),
                selectinload(UserProfile.otherPreference),
                selectinload(UserProfile.education),
                selectinload(UserProfile.certifications),
                selectinload(UserProfile.experience),
                selectinload(UserProfile.knownLanguages)
            )
            .filter(UserProfile.profileId == profile_id).first()
        )
        return user_profile.scalars().first()
        
        
    
    @staticmethod
    async def update_profile(db:Session, profile_id:int, updated_data):
        user_profile = ProfileService.get_user_profile(profile_id, id)
        if not user_profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_PROFILE_NOT_FOUND)

        updated_user_profile = update_user_profile(db, user_profile, updated_data)
        return updated_user_profile
    


    @staticmethod
    async def delete_user_profile(db, user_id):
        ...
        