from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    company_info_id = Column(Integer, ForeignKey('company_information.id'))
    street = Column(String)
    city = Column(String)
    landmark = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)

    company_info = relationship("CompanyInformation",
                                          back_populates="address")

class PersonalEmployerInformation(Base):
    __tablename__ = 'personal_employer_information'

    id = Column(Integer, primary_key=True, index=True)
    employer_profile_id = Column(String, ForeignKey(
        "employer_profiles.employer_id",
        ondelete="CASCADE"
    ))
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String)
    phone_number = Column(String)
    password = Column(String)
    position = Column(String)
    social_media_link = Column(String)
    gender = Column(String)

    employer_profile = relationship("EmployerProfile",
                                    back_populates="personal_information")

class CompanyInformation(Base):
    __tablename__ = 'company_information'

    id = Column(Integer, primary_key=True, index=True)
    employer_profile_id = Column(String, ForeignKey(
        "employer_profiles.employer_id"
    ))
    company_name = Column(String)
    industry = Column(String)
    company_size = Column(String)
    business_type = Column(String)
    company_phone_number = Column(String)
    company_website = Column(String)
    social_media_link = Column(String)
    desc = Column(String)
    address = relationship("Address", back_populates="company_info")

    employer_profile = relationship("EmployerProfile",
                                    back_populates="company_information")

class AdditionalInformation(Base):
    __tablename__ = 'additional_information'

    id = Column(Integer, primary_key=True, index=True)
    employer_profile_id = Column(String, ForeignKey(
        "employer_profiles.employer_id"
    ))
    hear_about_us = Column(String)
    agreed_to_terms = Column(String)

    employer_profile = relationship("EmployerProfile",
                                    back_populates="additional_information")

class EmployerProfile(Base):
    __tablename__ = 'employer_profiles'

    employer_id = Column(String, primary_key=True, index=True)
    personal_information = relationship("PersonalEmployerInformation", back_populates="employer_profile")
    company_information = relationship("CompanyInformation", back_populates="employer_profile")
    additional_information = relationship("AdditionalInformation", back_populates="employer_profile")
