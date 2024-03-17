from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    personal_info_id = Column(Integer, ForeignKey('personal_employer_information.id'))
    street = Column(String)
    city = Column(String)
    landmark = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)

class PersonalEmployerInformation(Base):
    __tablename__ = 'personal_employer_information'

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    username = Column(String)
    email = Column(String)
    phoneNumber = Column(String)
    password = Column(String)
    position = Column(String)
    socialMediaLink = Column(String)
    gender = Column(String)

class CompanyInformation(Base):
    __tablename__ = 'company_information'

    id = Column(Integer, primary_key=True, index=True)
    companyName = Column(String)
    industry = Column(String)
    companySize = Column(String)
    businessType = Column(String)
    companyPhoneNumber = Column(String)
    companyWebsite = Column(String)
    socialMediaLink = Column(String)
    desc = Column(String)
    address_id = Column(Integer, ForeignKey('addresses.id'))

    address = relationship("Address")

class AdditionalInformation(Base):
    __tablename__ = 'additional_information'

    id = Column(Integer, primary_key=True, index=True)
    hearAboutUs = Column(String)
    agreedToTerms = Column(String)

class EmployerProfile(Base):
    __tablename__ = 'employer_profiles'

    employer_id = Column(String, primary_key=True, index=True)
    personal_information_id = Column(Integer, ForeignKey('personal_employer_information.id'))
    company_information_id = Column(Integer, ForeignKey('company_information.id'))
    additional_information_id = Column(Integer, ForeignKey('additional_information.id'))

    personal_information = relationship("PersonalEmployerInformation")
    company_information = relationship("CompanyInformation")
    additional_information = relationship("AdditionalInformation")
