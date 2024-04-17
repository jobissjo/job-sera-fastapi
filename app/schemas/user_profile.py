from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from app.utils.database import Base

class PersonalDetail(Base):
    __tablename__ = 'personal_details'


    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey('user_profiles.profileId'))
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
    userProfileId = Column(String, ForeignKey('user_profiles.profileId'))
    jobType = Column(String)

    user_profile = relationship("UserProfile", back_populates="otherPreference")

class EducationType(Base):
    __tablename__ = 'education_types'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey('user_profiles.profileId'))
    level = Column(String)
    fieldOfStudy = Column(String)
    startedDate = Column(Date)
    endedDate = Column(Date)

    user_profile = relationship("UserProfile", back_populates="education")

class CertificationType(Base):
    __tablename__ = 'certification_types'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey('user_profiles.profileId'))
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
    userProfileId = Column(String, ForeignKey('user_profiles.profileId'))
    position = Column(String)
    companyName = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)

    user_profile = relationship("UserProfile", back_populates="experience")

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, index=True)
    userProfileId = Column(String, ForeignKey('user_profiles.profileId'))
    language = Column(String)
    level = Column(String)
    reading = Column(Boolean)
    writing = Column(Boolean)
    speaking = Column(Boolean)
    user_profile = relationship("UserProfile", back_populates="knownLanguages")


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    profileId = Column(String, primary_key=True, index=True)
    personalDetail = relationship("PersonalDetail", uselist=False, back_populates="user_profile", cascade="all, delete")
    otherPreference = relationship("OtherPreference", uselist=False, back_populates="user_profile", cascade="all, delete")
    education = relationship("EducationType", back_populates="user_profile", cascade="all, delete")
    certifications = relationship("CertificationType", back_populates="user_profile", cascade="all, delete")
    experience = relationship("Experience", back_populates="user_profile", cascade="all, delete")
    knownLanguages = relationship("Language", back_populates="user_profile", cascade="all, delete")
    skills = Column(JSON)
    preferredLocations = Column(JSON)
