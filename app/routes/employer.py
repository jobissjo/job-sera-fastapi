from fastapi import Depends, status,APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.models.employer import EmployerProfileType
from app.utils.database import get_db
from app.models.users import UserModel
from app.utils.auth import get_current_active_user
from app.schemas.employer import Address, CompanyInformation, PersonalEmployerInformation,AdditionalInformation, EmployerProfile

router = APIRouter(prefix='/employer', tags=['employer'])



@router.post('/')
async def create_employer(employer:EmployerProfileType,
                          db:Session = Depends(get_db),
                          current_user:UserModel = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to create a user profile")
    
    address_data = employer.companyInformation.address
    address_model = Address(**address_data.dict())
    db.add(address_model)
    db.flush()  # This flushes pending changes to the database so that the auto-generated ID is available
    
    company_information_data = employer.companyInformation
    company_information_model = CompanyInformation(**company_information_data.dict(), address_id=address_model.id)
    db.add(company_information_model)
    db.flush()
    
    personal_information_data = employer.personalInformation
    personal_information_model = PersonalEmployerInformation(**personal_information_data.dict())
    db.add(personal_information_model)
    db.flush()
    
    additional_information_data = employer.additionalInformation
    additional_information_model = AdditionalInformation(**additional_information_data.dict())
    db.add(additional_information_model)
    db.flush()
    
    # Create the employer profile model and associate the other models
    employer_profile_model = EmployerProfile(personal_information=personal_information_model,
                                              company_information=company_information_model,
                                              additional_information=additional_information_model)
    db.add(employer_profile_model)
    db.commit()  # Commit all changes to the database
    
    return {"message": "Employer profile created successfully"}


@router.get('/{id}')
async def get_employer_by_id():
    ...


@router.put('/{id}')
async def update_employer():
    ...

@router.delete('/{id}')
async def delete_employer():
    ...