from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    company_info_id = Column(String, ForeignKey('company_information.id'))
    street = Column(String)
    city = Column(String)
    landmark = Column(String)
    state = Column(String)
    country = Column(String)
    postalCode = Column(String)

    company_info = relationship("CompanyInformation",
                                          back_populates="address")

class PersonalEmployerInformation(Base):
    __tablename__ = 'personal_employer_information'

    id = Column(Integer, primary_key=True, index=True)
    employer_profile_id = Column(String, ForeignKey(
        "employer_profiles.employer_id",
        ondelete="CASCADE"
    ))
    firstName = Column(String)
    lastName = Column(String)
    username = Column(String)
    email = Column(String)
    phoneNumber = Column(String)
    # password = Column(String)
    position = Column(String)
    socialMediaLink = Column(String)
    gender = Column(String)

    employer_profile = relationship("EmployerProfile",
                                    back_populates="personalInformation")

class CompanyInformation(Base):
    __tablename__ = 'company_information'

    id = Column(Integer, primary_key=True, index=True)
    employer_profile_id = Column(String, ForeignKey(
        "employer_profiles.employer_id"
    ))
    companyName = Column(String)
    industry = Column(String)
    companySize = Column(String)
    businessType = Column(String)
    companyPhoneNumber = Column(String)
    companyWebsite = Column(String)
    socialMediaLink = Column(String)
    desc = Column(String)
    address = relationship("Address", back_populates="company_info")

    employer_profile = relationship("EmployerProfile",
                                    back_populates="companyInformation")

class AdditionalInformation(Base):
    __tablename__ = 'additional_information'

    id = Column(Integer, primary_key=True, index=True)
    employer_profile_id = Column(String, ForeignKey(
        "employer_profiles.employer_id"
    ))
    hearAboutUs = Column(String)
    agreedToTerms = Column(Boolean)

    employer_profile = relationship("EmployerProfile",
                                    back_populates="additionalInformation")

class EmployerProfile(Base):
    __tablename__ = 'employer_profiles'

    employer_id = Column(String, primary_key=True, index=True)
    personalInformation = relationship("PersonalEmployerInformation", back_populates="employer_profile", cascade="all, delete")
    companyInformation = relationship("CompanyInformation", back_populates="employer_profile", cascade="all, delete")
    additionalInformation = relationship("AdditionalInformation", back_populates="employer_profile", cascade="all, delete")
