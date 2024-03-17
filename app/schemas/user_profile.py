from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from app.utils.database import Base

class PersonalDetail(Base):
    __tablename__ = 'personal_details'

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(String, ForeignKey('user_profiles.profile_id'))
    name = Column(String)
    heading = Column(String)
    email = Column(String)
    phone_number = Column(String)
    dob = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    social_media_link = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    country = Column(String)
    state = Column(String)
    district = Column(String)
    postal_code = Column(String, nullable=True)

    user_profile = relationship("UserProfile", back_populates="personal_detail")

class OtherPreference(Base):
    __tablename__ = 'other_preferences'

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(String, ForeignKey('user_profiles.profile_id'))
    job_type = Column(String)

    user_profile = relationship("UserProfile", back_populates="other_preference")

class EducationType(Base):
    __tablename__ = 'education_types'

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(String, ForeignKey('user_profiles.profile_id'))
    level = Column(String)
    field_of_study = Column(String)
    started_date = Column(Date)
    ended_date = Column(Date)

    user_profile = relationship("UserProfile", back_populates="education")

class CertificationType(Base):
    __tablename__ = 'certification_types'

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(String, ForeignKey('user_profiles.profile_id'))
    title = Column(String)
    certificate_id = Column(String)
    mode = Column(String)
    institution = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    user_profile = relationship("UserProfile", back_populates="certifications")

class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(String, ForeignKey('user_profiles.profile_id'))
    position = Column(String)
    company_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    user_profile = relationship("UserProfile", back_populates="experience")

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(String, ForeignKey('user_profiles.profile_id'))
    language = Column(String)
    level = Column(String)
    reading = Column(Boolean)
    writing = Column(Boolean)
    speaking = Column(Boolean)

    user_profile = relationship("UserProfile", back_populates="known_languages")

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    profile_id = Column(String, primary_key=True, index=True)
    personal_detail = relationship("PersonalDetail", uselist=False, back_populates="user_profile")
    other_preference = relationship("OtherPreference", uselist=False, back_populates="user_profile")
    education = relationship("EducationType", back_populates="user_profile")
    certifications = relationship("CertificationType", back_populates="user_profile")
    experience = relationship("Experience", back_populates="user_profile")
    known_languages = relationship("Language", back_populates="user_profile")
    skills = Column(JSON)
    preferred_locations = Column(JSON)
