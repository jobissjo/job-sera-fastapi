from fastapi import Depends, status,APIRouter, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.employer import EmployerProfileType, ResponseEmployerProfileType
from app.core.database import get_db
from app.models.users import  ResponseUser
from app.utils.auth import get_current_active_user
from app.schemas.employer import Address, CompanyInformation, PersonalEmployerInformation,AdditionalInformation, EmployerProfile
from app.crud.employer import delete_employer_profile
from app.utils.constants import EMPLOYER_PROFILE_NOT_FOUND

router = APIRouter(prefix='/employer', tags=['Employer'])



def get_by_id(employer_id: str, db: Session)->ResponseEmployerProfileType:

    employer = db.query(EmployerProfile).options(
        joinedload(EmployerProfile.personalInformation),
        joinedload(EmployerProfile.companyInformation),
        joinedload(EmployerProfile.additionalInformation)
    ).filter(EmployerProfile.employer_id == employer_id).first()


    return employer
@router.post('/')
async def create_employer(employer: EmployerProfileType,
                          db: Session = Depends(get_db),
                          current_user: ResponseUser = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to create an employer profile")
    if current_user.role != 'employer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Your profile is not an employer profile")

    # Check if the current user id matches the employer id
    if current_user.id != employer.employer_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="User id and employer id do not match")

    # Create PersonalEmployerInformation object
    personal_info = PersonalEmployerInformation(**employer.personalInformation.dict())

    # Create CompanyInformation object
    company_info_data = employer.companyInformation.dict()
    address_data = company_info_data.pop('address')

    # Create Address objects
    address_objects = [Address(**address_data)]

    company_info = CompanyInformation(**company_info_data, address=address_objects)

    # Create AdditionalInformation object
    additional_info = AdditionalInformation(**employer.additionalInformation.dict())

    # Create EmployerProfile object
    employer_profile = EmployerProfile(
        employer_id=employer.employer_id,
        personalInformation=[personal_info],
        companyInformation=[company_info],
        additionalInformation=[additional_info]
    )

    # Add and commit to the database
    db.add(employer_profile)
    db.commit()
    db.refresh(employer_profile)

    return {"message": "Employer profile created successfully"}


@router.get('/{employer_id}')
async def get_employer_by_id(employer_id: str, db: Session = Depends(get_db)):
    # Retrieve the employer profile from the database based on the provided ID
    employer_profile = db.query(EmployerProfile).options(
        joinedload(EmployerProfile.personalInformation),
        joinedload(EmployerProfile.companyInformation).joinedload(CompanyInformation.address),
        joinedload(EmployerProfile.additionalInformation)
    ).filter(EmployerProfile.employer_id == employer_id).first()
    # Check if the employer profile exists
    if not employer_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EMPLOYER_PROFILE_NOT_FOUND)
    return employer_profile





@router.put('/{employer_id}', response_model=EmployerProfileType)
async def update_employer(employer_id: str, updated_employer: EmployerProfileType,_current_user:Session= Depends(get_current_active_user),
                          db:Session = Depends(get_db)):
    employer_profile = get_by_id(employer_id, db)

    if not employer_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EMPLOYER_PROFILE_NOT_FOUND) 

    employer_profile.personalInformation = [PersonalEmployerInformation(**updated_employer.personalInformation.dict())]
    company_info_data = updated_employer.companyInformation.dict()
    address_data = company_info_data.pop('address')

    # Create Address objects
    address_objects = [Address(**address_data)]
    employer_profile.companyInformation = [CompanyInformation(**company_info_data,address=address_objects)]
    employer_profile.additionalInformation = [AdditionalInformation(**updated_employer.additionalInformation.dict())]

    db.commit()
    db.refresh(employer_profile)
    return updated_employer
    
@router.delete('/{id}')
async def delete_employer(employer_id: str, _current_user:Session= Depends(get_current_active_user),
                          db:Session = Depends(get_db)):
    employer_profile = get_by_id(employer_id, db)

    if not employer_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EMPLOYER_PROFILE_NOT_FOUND)
    delete_employer_profile(db,employer_profile)

    return {'message': 'Employer Profile deleted successfully'}