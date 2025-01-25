from fastapi import Depends, status,APIRouter, HTTPException
from app.schema.company import CompanyModel
from sqlalchemy.orm import Session, joinedload
from app.utils.auth import get_current_employer
from app.core.database import get_db
from app.models.company import Review, Company
from app.utils.constants import COMPANY_NOT_FOUND


router = APIRouter(prefix='/company', tags=['Company'])


@router.post('/')
async def create_company(company:CompanyModel, db:Session = Depends(get_db),
                         employer:Session = Depends(get_current_employer)):
    if not employer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="You are not allowed in this page")
    company_dict = company.model_dump()   
    if len(company.reviews):
        review_data = company_dict.pop('reviews')
        reviews = [Review(**review) for review in review_data]
        company = Company(**company_dict,reviews=reviews )
    else:
        company = Company(**company_dict)
    db.add(company)
    db.commit()
    db.refresh(company)

    return {"message": "Company profile created successfully"}

@router.get('/', response_model=list[CompanyModel])
async def get_companies(db: Session= Depends(get_db)):
    companies = db.query(Company).all()

    return companies

@router.get('/{company_id}', response_model=CompanyModel)
async def get_company_id(company_id:str, db:Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=COMPANY_NOT_FOUND)
    return company

def company_to_dict(company):
    return {column.name: getattr(company, column.name) for column in company.__table__.columns}




@router.put('/{company_id}')
async def update_company(company_id: str, updated_company_detail: CompanyModel, db: Session = Depends(get_db), 
                         current_employer: Session = Depends(get_current_employer)):
    # Fetch the company object from the database
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=COMPANY_NOT_FOUND)

    # Update company attributes
    

    for field, value in updated_company_detail.dict().items():
        if field == 'reviews':
            if len(value):
                for val in value:  
                    rev = [Review(**val, company_id=company.id)]
                    setattr(company, field, rev)
        else:
            setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company

@router.delete('/{company_id}')
async def delete_company(company_id:str, db:Session = Depends(get_db), 
                         current_employer:Session = Depends(get_current_employer)):
    company = db.query(Company).options(joinedload(Company.reviews)).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=COMPANY_NOT_FOUND)

    db.delete(company)
    db.commit()

    return {'message': "Company is deleted successfully"}
    