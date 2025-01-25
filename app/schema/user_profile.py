from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class PersonalDetail(BaseModel):
    name: str
    heading: str
    email: str
    phoneNumber: str
    dob: Optional[date] = None
    gender: Optional[str] = None
    socialMediaLink: Optional[str] = None
    githubLink: Optional[str] = None
    country: str
    state: str
    district: str
    postalCode: Optional[str] = None


class OtherPreference(BaseModel):
    jobType: str


class EducationType(BaseModel):
    level: str
    fieldOfStudy: str
    startedDate: date
    endedDate: date


class CertificationType(BaseModel):
    title: str
    certificateId: str
    mode: str
    institution: str
    startDate: date
    endDate: date


class Experience(BaseModel):
    position: str
    companyName: str
    startDate: date
    endDate: date


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
