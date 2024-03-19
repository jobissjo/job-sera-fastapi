from app.schemas.employer import EmployerProfile
from app.models.employer import EmployerProfileType
from sqlalchemy.orm import Session

def update_employer_profile(db:Session, employer_profile: EmployerProfile, updated_employer:EmployerProfileType):
    
    updated_employer.company_information.address = [updated_employer.company_information.model_dump().pop('address')]
    print("i just started here")
    employer_profile.company_information = [updated_employer.company_information.dict()]
    print("i completed a company info")
    employer_profile.additional_information = [updated_employer.additional_information]
    employer_profile.personal_information = [updated_employer.personal_information]
    print("here i reached")
    db.commit()
    db.refresh(employer_profile)
    return employer_profile

def delete_employer_profile(db: Session, employer_profile:EmployerProfile):
    db.delete(employer_profile)
    db.commit()