from typing import List, Optional
from pydantic import BaseModel


class PersonalDetail(BaseModel):
    name: str
    heading: str
    email: str
    phoneNumber: str
    dob: Optional[str] = None
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
    startedDate: str
    endedDate: str


class CertificationType(BaseModel):
    title: str
    certificateId: str
    mode: str
    institution: str
    startDate: str
    endDate: str


class Experience(BaseModel):
    position: str
    companyName: str
    startDate: str
    endDate: str


class Language(BaseModel):
    language: str
    level: str
    reading: bool
    writing: bool
    speaking: bool


class UserProfile(BaseModel):
    profileId: Optional[str]
    personalDetail: PersonalDetail
    education: List[EducationType]
    certifications: List[CertificationType]
    skills: List[str]
    experience: List[Experience]
    knownLanguages: List[Language]
    preferredLocations: List[str]
    otherPreference: OtherPreference
