from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class PersonalDetail(BaseModel):
    name: str
    heading: str
    email: str
    phone_number: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    social_media_link: Optional[str] = None
    github_link: Optional[str] = None
    country: str
    state: str
    district: str
    postal_code: Optional[str] = None


class OtherPreference(BaseModel):
    job_type: str


class EducationType(BaseModel):
    level: str
    field_of_study: str
    started_date: date
    ended_date: date


class CertificationType(BaseModel):
    title: str
    certificate_id: str
    mode: str
    institution: str
    start_date: date
    end_date: date


class Experience(BaseModel):
    position: str
    company_name: str
    start_date: date
    end_date: date


class Language(BaseModel):
    language: str
    level: str
    reading: bool
    writing: bool
    speaking: bool


class UserProfileModel(BaseModel):
    profileId: str
    personalDetail: PersonalDetail
    education: List[EducationType]
    certifications: List[CertificationType]
    skills: List[str]
    experience: List[Experience]
    knownLanguages: List[Language]
    preferredLocations: List[str]
    otherPreference: OtherPreference
