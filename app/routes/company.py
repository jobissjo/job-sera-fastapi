from fastapi import Depends, status,APIRouter, HTTPException
from app.models.company import CompanyModel
from sqlalchemy.orm import Session
from app.utils.auth import get_current_employer
from app.utils.database import get_db


router = APIRouter(prefix='/company', tags=['company'])


@router.post('/')
async def create_company(company:CompanyModel, db:Session = Depends(get_db),
                         employer:Session = Depends(get_current_employer)):
    ...

@router.get('/')
async def get_companies(db: Session= Depends(get_db)):
    ...

@router.get('/{company_id}')
async def get_company_id(company_id:str, db:Session = Depends(get_db)):
    ...

@router.put('/{company_id}')
async def update_company(company_id:str, db:Session = Depends(get_db), 
                         current_employer:Session = Depends(get_current_employer)):
    ...


@router.delete('/{company_id}')
async def delete_company(company_id:str, db:Session = Depends(get_db), 
                         current_employer:Session = Depends(get_current_employer)):
    ...

