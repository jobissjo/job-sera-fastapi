from app.models.employer import EmployerProfile
from app.schema.employer import EmployerProfileType
from sqlalchemy.orm import Session

def update_employer_profile(db:Session, employer_profile: EmployerProfile, updated_employer:EmployerProfileType):
    
    updated_employer.companyInformation.address = [updated_employer.companyInformation.model_dump().pop('address')]

    employer_profile.companyInformation = [updated_employer.companyInformation.dict()]
    employer_profile.additionalInformation = [updated_employer.additionalInformation]
    employer_profile.personalInformation = [updated_employer.personalInformation]
    db.commit()
    db.refresh(employer_profile)
    return employer_profile

def delete_employer_profile(db: Session, employer_profile:EmployerProfile):
    db.delete(employer_profile)
    db.commit()