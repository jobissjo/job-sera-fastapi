from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.employer import EmployerProfileType
from app.core.database import get_db
from app.utils.auth import get_current_active_user
from app.services.employer_service import EmployerService

router = APIRouter(prefix="/employer", tags=["Employer"])


@router.post("/")
async def create_employer(
    employer: EmployerProfileType,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return await EmployerService.create_employer(employer, current_user, db)


@router.get("/{employer_id}")
async def get_employer_by_id(employer_id: str, db: AsyncSession = Depends(get_db)):
    employer_profile = await EmployerService.get_by_id(employer_id, db)
    if not employer_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employer profile not found"
        )
    return employer_profile


@router.put("/{employer_id}")
async def update_employer(
    employer_id: str,
    updated_employer: EmployerProfileType,
    db: AsyncSession = Depends(get_db),
):
    return await EmployerService.update_employer(employer_id, updated_employer, db)


@router.delete("/{employer_id}")
async def delete_employer(employer_id: str, db: AsyncSession = Depends(get_db)):
    return await EmployerService.delete_employer(employer_id, db)
