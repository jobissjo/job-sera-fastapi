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
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: str
    position: str
    social_media_link: str
    gender: str

class CompanyInformation(BaseModel):
    company_name: str
    industry: str
    company_size: str
    business_type: str
    company_phone_number: str
    company_website: str
    social_media_link: str
    desc: str
    address: Address

class AdditionalInformation(BaseModel):
    hear_about_us: str
    agreed_to_terms: str

class EmployerProfileType(BaseModel):
    employer_id:str
    personal_information: PersonalInformation
    company_information: CompanyInformation
    additional_information: AdditionalInformation
