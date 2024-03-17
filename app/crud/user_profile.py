from sqlalchemy.orm import Session, joinedload
from app.schemas.user_profile import UserProfile
from app.models.user_profile import UserProfileModel



def update_user_profile(db: Session, user_profile: UserProfileModel, user_profile_data: UserProfileModel) -> UserProfileModel:
    for field, value in user_profile_data.model_dump().items():
        setattr(user_profile, field, value)
    db.commit()
    db.refresh(user_profile)
    return user_profile


def delete_user_profile(db: Session, user_profile: UserProfile):
    db.delete(user_profile)
    db.commit()
