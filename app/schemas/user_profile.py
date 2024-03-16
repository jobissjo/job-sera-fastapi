from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PersonalDetail(Base):
    __tablename__ = 'personal_details'

    id = Column(Integer, primary_key=True, index=True)
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

class OtherPreference(Base):
    __tablename__ = 'other_preferences'

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String)

class EducationType(Base):
    __tablename__ = 'education_types'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('personal_details.id'))
    level = Column(String)
    field_of_study = Column(String)
    started_date = Column(Date)
    ended_date = Column(Date)

class CertificationType(Base):
    __tablename__ = 'certification_types'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('personal_details.id'))
    title = Column(String)
    certificate_id = Column(String)
    mode = Column(String)
    institution = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('personal_details.id'))
    position = Column(String)
    company_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('personal_details.id'))
    language = Column(String)
    level = Column(String)
    reading = Column(Boolean)
    writing = Column(Boolean)
    speaking = Column(Boolean)

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    profile_id = Column(String, primary_key=True, index=True)
    personal_detail_id = Column(Integer, ForeignKey('personal_details.id'))
    education = relationship("EducationType")
    certifications = relationship("CertificationType")
    skills = Column(String)
    experience = relationship("Experience")
    known_languages = relationship("Language")
    preferred_locations = Column(String)  # Assuming it's a comma-separated string of locations
    other_preference_id = Column(Integer, ForeignKey('other_preferences.id'))

    personal_detail = relationship("PersonalDetail", back_populates="user_profile")
    other_preference = relationship("OtherPreference", back_populates="user_profile")

PersonalDetail.user_profile = relationship("UserProfile", back_populates="personal_detail")
OtherPreference.user_profile = relationship("UserProfile", back_populates="other_preference")
