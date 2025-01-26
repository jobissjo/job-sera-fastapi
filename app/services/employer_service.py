from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from app.models.employer import (
    EmployerProfile,
    PersonalEmployerInformation,
    CompanyInformation,
    Address,
    AdditionalInformation
)
from app.schema.employer import EmployerProfileType
from app.utils.constants import EMPLOYER_PROFILE_NOT_FOUND


class EmployerService:
    @staticmethod
    async def get_by_id(employer_id: str, db: AsyncSession):
        query = (
            select(EmployerProfile)
            .options(
                joinedload(EmployerProfile.personalInformation),
                joinedload(EmployerProfile.companyInformation).joinedload(CompanyInformation.address),
                joinedload(EmployerProfile.additionalInformation)
            )
            .filter(EmployerProfile.employer_id == employer_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_employer(employer: EmployerProfileType, current_user, db: AsyncSession):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You must be logged in to create an employer profile",
            )
        if current_user.role != "employer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your profile is not an employer profile",
            )
        if current_user.id != employer.employer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User id and employer id do not match",
            )

        # Create necessary objects
        personal_info = PersonalEmployerInformation(**employer.personalInformation.dict())
        company_info_data = employer.companyInformation.dict()
        address_data = company_info_data.pop("address")
        address_objects = [Address(**address_data)]
        company_info = CompanyInformation(**company_info_data, address=address_objects)
        additional_info = AdditionalInformation(**employer.additionalInformation.dict())

        # Create EmployerProfile object
        employer_profile = EmployerProfile(
            employer_id=employer.employer_id,
            personalInformation=[personal_info],
            companyInformation=[company_info],
            additionalInformation=[additional_info],
        )

        # Add and commit to the database
        db.add(employer_profile)
        await db.commit()
        await db.refresh(employer_profile)

        return {"message": "Employer profile created successfully"}

    @staticmethod
    async def update_employer(employer_id: str, updated_employer: EmployerProfileType, db: AsyncSession):
        employer_profile = await EmployerService.get_by_id(employer_id, db)
        if not employer_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=EMPLOYER_PROFILE_NOT_FOUND
            )

        # Update fields
        employer_profile.personalInformation = [
            PersonalEmployerInformation(**updated_employer.personalInformation.dict())
        ]
        company_info_data = updated_employer.companyInformation.dict()
        address_data = company_info_data.pop("address")
        address_objects = [Address(**address_data)]
        employer_profile.companyInformation = [
            CompanyInformation(**company_info_data, address=address_objects)
        ]
        employer_profile.additionalInformation = [
            AdditionalInformation(**updated_employer.additionalInformation.dict())
        ]

        await db.commit()
        await db.refresh(employer_profile)
        return updated_employer

    @staticmethod
    async def delete_employer(employer_id: str, db: AsyncSession):
        employer_profile = await EmployerService.get_by_id(employer_id, db)
        if not employer_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=EMPLOYER_PROFILE_NOT_FOUND
            )

        await db.delete(employer_profile)
        await db.commit()
        return {"message": "Employer Profile deleted successfully"}
