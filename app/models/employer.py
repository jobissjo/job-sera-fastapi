from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    landmark: str
    state: str
    country: str
    postalCode: str

class PersonalInformation(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    phoneNumber: str
    position: str
    socialMediaLink: str
    gender: str

class CompanyInformation(BaseModel):
    companyName: str
    industry: str
    companySize: str
    businessType: str
    companyPhoneNumber: str
    companyWebsite: str
    socialMediaLink: str
    desc: str
    address: Address

class AdditionalInformation(BaseModel):
    hearAboutUs: str
    agreedToTerms: str

class EmployerProfileType(BaseModel):
    employer_id:str
    personalInformation: PersonalInformation
    companyInformation: CompanyInformation
    additionalInformation: AdditionalInformation

class ResponseEmployerProfileType(BaseModel):
    employer_id:str
    personalInformation: list[PersonalInformation]
    companyInformation: list[CompanyInformation]
    additionalInformation: list[AdditionalInformation]