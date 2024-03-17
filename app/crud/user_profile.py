from sqlalchemy.orm import Session, joinedload
from app.models.user_profile import UserProfileModel as UserProfileDB
from app.schemas.user_profile import UserProfile as UserProfileSchema
from app.models.user_profile import UserProfileModel

def get_user_profile_by_id(db: Session, profile_id: str) -> UserProfileSchema:
    user_profile = db.query(UserProfileSchema).options(
        joinedload(UserProfileSchema.personal_detail),
        joinedload(UserProfileSchema.other_preference),
        joinedload(UserProfileSchema.education),
        joinedload(UserProfileSchema.certifications),
        joinedload(UserProfileSchema.experience),
        joinedload(UserProfileSchema.known_languages)
    ).filter(UserProfileSchema.profile_id == profile_id).first()

    print(user_profile, user_profile.__dict__, user_profile.__tablename__)
    return user_profile



def update_user_profile(db: Session, user_profile: UserProfileSchema, user_profile_data: UserProfileSchema) -> UserProfileModel:
    for field, value in user_profile_data.dict().items():
        setattr(user_profile, field, value)
    db.commit()
    db.refresh(user_profile)
    return user_profile


def delete_user_profile(db: Session, user_profile: UserProfileSchema):
    db.delete(user_profile)
    db.commit()
