from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    landmark: str
    state: str
    country: str
    postal_code: str

class PersonalInformation(BaseModel):
    firstName: str
    lastName: str
    username: str
    email: str
    phone_number: str
    position: str
    social_media_link: str
    gender: str

class CompanyInformation(BaseModel):
    company_name: str
    industry: str
    companySize: str
    businessType: str
    company_phone_number: str
    company_Website: str
    social_media_link: str
    desc: str
    address: Address

class AdditionalInformation(BaseModel):
    hear_about_us: str
    agreed_to_terms: str

class EmployerProfileType(BaseModel):
    employer_id:str
    personalInformation: PersonalInformation
    companyInformation: CompanyInformation
    additionalInformation: AdditionalInformation
