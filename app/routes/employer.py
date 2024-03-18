from fastapi import Depends, status,APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.models.employer import EmployerProfileType
from app.utils.database import get_db
from app.models.users import UserModel, ResponseUser
from app.utils.auth import get_current_active_user
from app.schemas.employer import Address, CompanyInformation, PersonalEmployerInformation,AdditionalInformation, EmployerProfile
from app.utils.employer import employer_profile_model_schemas


router = APIRouter(prefix='/employer', tags=['employer'])





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
    personal_info = PersonalEmployerInformation(**employer.personal_information.dict())

    # Create CompanyInformation object
    company_info_data = employer.company_information.dict()
    address_data = company_info_data.pop('address')
    print(address_data)
    address = Address(**address_data)
    print(address, company_info_data)
    company_info = CompanyInformation(**company_info_data, address=address)
    print("reached here")
    # Create AdditionalInformation object
    additional_info = AdditionalInformation(**employer.additional_information.dict())

    # Create EmployerProfile object
    employer_profile = EmployerProfile(
        employer_id=employer.employer_id,
        personal_information=personal_info,
        company_information=company_info,
        additional_information=additional_info
    )

    # Add and commit to the database
    db.add(employer_profile)
    db.commit()
    db.refresh(employer_profile)

    return {"message": "Employer profile created successfully"}

@router.get('/{id}')
async def get_employer_by_id(id:str, db: Session= Depends(get_db)):
    ...


@router.put('/{id}')
async def update_employer():
    ...

@router.delete('/{id}')
async def delete_employer():
    ...