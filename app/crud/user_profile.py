from sqlalchemy.orm import Session
from app.models.user_profile import (EducationType, Language, UserProfile, 
                                      CertificationType, OtherPreference, PersonalDetail,
                                      Experience)
from app.schema.user_profile import UserProfileModel



def update_user_profile(db: Session, user_profile: UserProfile, 
                        user_profile_data: UserProfileModel) -> UserProfileModel:
    user_profile.certifications = [CertificationType(**cert.model_dump(), 
                                                     userProfileId=user_profile.profileId
                                                     ) for cert in user_profile_data.certifications]
    user_profile.knownLanguages = [Language(**lang.model_dump(), 
                                            userProfileId=user_profile.profileId
                                            ) for lang in user_profile_data.knownLanguages]
    user_profile.education = [EducationType(**edu.model_dump(), 
                                            userProfileId=user_profile.profileId
                                            ) for edu in user_profile_data.education]
    user_profile.experience = [Experience(**exp.model_dump()) for exp in user_profile_data.experience]
    user_profile.preferredLocations = user_profile_data.preferredLocations
    user_profile.otherPreference = OtherPreference(**user_profile_data.otherPreference.model_dump(),
                                                   userProfileId=user_profile.profileId)
    user_profile.personalDetail = PersonalDetail(**user_profile_data.personalDetail.model_dump(),
                                                 userProfileId=user_profile.profileId)
    user_profile.skills = user_profile_data.skills
    db.commit()
    db.refresh(user_profile)
    return user_profile


def delete_user_profile(db: Session, user_profile: UserProfile):
    db.delete(user_profile)
    db.commit()
