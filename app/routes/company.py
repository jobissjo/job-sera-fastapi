# company_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schema.company import CompanyModel
from app.core.database import get_db
from app.utils.auth import get_current_employer
from app.services.company_service import CompanyService

router = APIRouter(prefix="/company", tags=["Company"])

@router.post("/")
async def create_company(
    company: CompanyModel, 
    db: Session = Depends(get_db), 
    employer: Session = Depends(get_current_employer)
):
    return await CompanyService.create_company(company, db, employer)

@router.get("/", response_model=list[CompanyModel])
async def get_companies(db: Session = Depends(get_db)):
    return await CompanyService.get_companies(db)

@router.get("/{company_id}", response_model=CompanyModel)
async def get_company(company_id: str, db: Session = Depends(get_db)):
    return await CompanyService.get_company_by_id(company_id, db)

@router.put("/{company_id}")
async def update_company(
    company_id: str, 
    updated_company_detail: CompanyModel, 
    db: Session = Depends(get_db)
):
    return await CompanyService.update_company(company_id, updated_company_detail, db)

@router.delete("/{company_id}")
async def delete_company(
    company_id: str, 
    db: Session = Depends(get_db), 
    employer: Session = Depends(get_current_employer)
):
    return await CompanyService.delete_company(company_id, db)
