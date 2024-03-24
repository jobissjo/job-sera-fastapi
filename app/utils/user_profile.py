
from app.schemas.user_profile import UserProfile,PersonalDetail, OtherPreference, EducationType, CertificationType, Experience, Language
from app.models.user_profile import UserProfileModel



def profile_model_schemas(user_profile_model:UserProfileModel)->UserProfile:
    profile_id = user_profile_model.profileId
    personal_detail_data = user_profile_model.personalDetail
    education_data = user_profile_model.education
    certifications_data = user_profile_model.certifications
    skills_data = user_profile_model.skills
    experience_data = user_profile_model.experience
    known_languages_data = user_profile_model.knownLanguages
    preferred_locations_data = user_profile_model.preferredLocations
    other_preference_data = user_profile_model.otherPreference

    # Create PersonalDetail object
    personal_detail = PersonalDetail(**personal_detail_data.dict(),user_profile_id=profile_id)
    
    # Create OtherPreference object
    other_preference = OtherPreference(**other_preference_data.dict(),user_profile_id=profile_id)
    
    # Create EducationType objects
    education_objects = [EducationType(**edu.dict(), user_profile_id=profile_id) for edu in education_data]

    # Create CertificationType objects
    certification_objects = [CertificationType(**cert.dict(), user_profile_id=profile_id) for cert in certifications_data]

    # Create Experience objects
    experience_objects = [Experience(**exp.dict(), user_profile_id=profile_id) for exp in experience_data]

    # Create Language objects
    language_objects = [Language(**lang.dict(), user_profile_id=profile_id) for lang in known_languages_data]

    # Create UserProfile object
    user_profile = UserProfile(
        profile_id=profile_id,
        personal_detail=personal_detail,
        education=education_objects,
        certifications=certification_objects,
        skills=skills_data,
        experience=experience_objects,
        known_languages=language_objects,
        preferred_locations=preferred_locations_data,
        other_preference=other_preference
    )

    return user_profile