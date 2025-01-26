from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.company import Company, Review
from app.schema.company import CompanyModel
from app.utils.constants import COMPANY_NOT_FOUND

class CompanyService:
    @staticmethod
    async def create_company(company_data: CompanyModel, db: AsyncSession, employer):
        if not employer:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="You are not allowed in this page")
        
        company_dict = company_data.model_dump()
        if len(company_data.reviews):
            review_data = company_dict.pop('reviews')
            reviews = [Review(**review) for review in review_data]
            company = Company(**company_dict, reviews=reviews)
        else:
            company = Company(**company_dict)
        
        db.add(company)
        await db.commit()
        await db.refresh(company)

        return {"message": "Company profile created successfully"}

    @staticmethod
    async def get_companies(db: AsyncSession):
        result = await db.execute(db.query(Company))
        return result.scalars().all()

    @staticmethod
    async def get_company_by_id(company_id: str, db: AsyncSession):
        result = await db.execute(db.query(Company).filter(Company.id == company_id))
        company = result.scalar()
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=COMPANY_NOT_FOUND)
        return company

    @staticmethod
    async def update_company(company_id: str, updated_company_detail: CompanyModel, db: AsyncSession):
        result = await db.execute(db.query(Company).filter(Company.id == company_id))
        company = result.scalar()
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=COMPANY_NOT_FOUND)

        for field, value in updated_company_detail.dict().items():
            if field == 'reviews' and len(value):
                reviews = [Review(**review, company_id=company.id) for review in value]
                setattr(company, field, reviews)
            else:
                setattr(company, field, value)

        await db.commit()
        await db.refresh(company)
        return company

    @staticmethod
    async def delete_company(company_id: str, db: AsyncSession):
        result = await db.execute(db.query(Company).filter(Company.id == company_id))
        company = result.scalar()
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=COMPANY_NOT_FOUND)
        
        await db.delete(company)
        await db.commit()
        return {"message": "Company is deleted successfully"}
