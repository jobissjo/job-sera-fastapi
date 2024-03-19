from fastapi import Depends, status,APIRouter, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.employer import EmployerProfileType
from app.utils.database import get_db
from app.models.users import UserModel, ResponseUser
from app.utils.auth import get_current_active_user
from app.schemas.employer import Address, CompanyInformation, PersonalEmployerInformation,AdditionalInformation, EmployerProfile
from app.utils.employer import employer_profile_model_schemas
from app.crud.employer import update_employer_profile, delete_employer_profile

router = APIRouter(prefix='/employer', tags=['employer'])



def get_by_id(employer_id: str, db: Session)->EmployerProfile:

    employer = db.query(EmployerProfile).options(
        joinedload(EmployerProfile.personal_information),
        joinedload(EmployerProfile.company_information),
        joinedload(EmployerProfile.additional_information)
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
    personal_info = PersonalEmployerInformation(**employer.personal_information.dict())

    # Create CompanyInformation object
    company_info_data = employer.company_information.dict()
    address_data = company_info_data.pop('address')

    # Create Address objects
    address_objects = [Address(**address_data)]

    company_info = CompanyInformation(**company_info_data, address=address_objects)

    # Create AdditionalInformation object
    additional_info = AdditionalInformation(**employer.additional_information.dict())

    # Create EmployerProfile object
    employer_profile = EmployerProfile(
        employer_id=employer.employer_id,
        personal_information=[personal_info],
        company_information=[company_info],
        additional_information=[additional_info]
    )

    # Add and commit to the database
    db.add(employer_profile)
    db.commit()
    db.refresh(employer_profile)

    return {"message": "Employer profile created successfully"}


@router.get('/{employer_id}', )
async def get_employer_by_id(employer_id: str, db: Session = Depends(get_db)):
    # Retrieve the employer profile from the database based on the provided ID
    employer_profile = db.query(EmployerProfile).options(
        joinedload(EmployerProfile.personal_information),
        joinedload(EmployerProfile.company_information),
        joinedload(EmployerProfile.additional_information)
    ).filter(EmployerProfile.employer_id == employer_id).first()

    # Check if the employer profile exists
    if not employer_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer profile not found")
    return employer_profile





@router.put('/{employer_id}')
async def update_employer(employer_id: str, updated_employer: EmployerProfileType,_current_user:Session= Depends(get_current_active_user),
                          db:Session = Depends(get_db)):
    employer_profile = get_by_id(employer_id, db)

    if not employer_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer profile not found") 

    employer_profile.personal_information = [PersonalEmployerInformation(**updated_employer.personal_information.dict())]
    company_info_data = updated_employer.company_information.dict()
    address_data = company_info_data.pop('address')

    # Create Address objects
    address_objects = [Address(**address_data)]
    employer_profile.company_information = [CompanyInformation(**company_info_data,address=address_objects)]
    employer_profile.additional_information = [AdditionalInformation(**updated_employer.additional_information.dict())]

    db.commit()
    db.refresh(employer_profile)
    return updated_employer
    
@router.delete('/{id}')
async def delete_employer(employer_id: str, _current_user:Session= Depends(get_current_active_user),
                          db:Session = Depends(get_db)):
    employer_profile = get_by_id(employer_id, db)

    if not employer_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer profile not found")
    delete_employer_profile(db,employer_profile)

    return {'message': 'Employer Profile deleted successfully'}