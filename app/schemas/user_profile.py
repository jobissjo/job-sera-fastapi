from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.utils.constants import ON_DELETE

USER_PROFILE_ID = "user_profiles.profileId"

class PersonalDetail(Base):
    __tablename__ = 'personal_details'


    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey(USER_PROFILE_ID))
    name = Column(String)
    heading = Column(String)
    email = Column(String)
    phoneNumber = Column(String)
    dob = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    socialMediaLink = Column(String, nullable=True)
    githubLink = Column(String, nullable=True)
    country = Column(String)
    state = Column(String)
    district = Column(String)
    postalCode = Column(String, nullable=True)

    user_profile = relationship("UserProfile", 
                                back_populates="personalDetail")

class OtherPreference(Base):
    __tablename__ = 'other_preferences'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey(USER_PROFILE_ID))
    jobType = Column(String)

    user_profile = relationship("UserProfile", back_populates="otherPreference")

class EducationType(Base):
    __tablename__ = 'education_types'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey(USER_PROFILE_ID))
    level = Column(String)
    fieldOfStudy = Column(String)
    startedDate = Column(Date)
    endedDate = Column(Date)

    user_profile = relationship("UserProfile", back_populates="education")

class CertificationType(Base):
    __tablename__ = 'certification_types'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey(USER_PROFILE_ID))
    title = Column(String)
    certificateId = Column(String)
    mode = Column(String)
    institution = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)

    user_profile = relationship("UserProfile", back_populates="certifications")

class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey(USER_PROFILE_ID))
    position = Column(String)
    companyName = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)

    user_profile = relationship("UserProfile", back_populates="experience")

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey(USER_PROFILE_ID))
    language = Column(String)
    level = Column(String)
    reading = Column(Boolean)
    writing = Column(Boolean)
    speaking = Column(Boolean)
    user_profile = relationship("UserProfile", back_populates="knownLanguages")


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    profileId = Column(String, primary_key=True, index=True)
    personalDetail = relationship("PersonalDetail", uselist=False, back_populates="user_profile", cascade=ON_DELETE)
    otherPreference = relationship("OtherPreference", uselist=False, back_populates="user_profile", cascade=ON_DELETE)
    education = relationship("EducationType", back_populates="user_profile", cascade=ON_DELETE)
    certifications = relationship("CertificationType", back_populates="user_profile", cascade=ON_DELETE)
    experience = relationship("Experience", back_populates="user_profile", cascade=ON_DELETE)
    knownLanguages = relationship("Language", back_populates="user_profile", cascade=ON_DELETE)
    skills = Column(JSON)
    preferredLocations = Column(JSON)
