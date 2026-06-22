from . import mcp
from app.schema.company import CompanyModel
from app.services.company_service import CompanyService
from app.core.database import get_db
from app.schema.common import McpCommonResponse
from typing import Optional


@mcp.tool
async def create_company(
    company_name: str,
    industry: str,
    description: str,
    website: Optional[str] = None,
    location: Optional[str] = None,
    employee_count: Optional[str] = None,
) -> McpCommonResponse:
    """
    Create a new company in the system.

    Args:
        company_name: Name of the company
        industry: Industry type
        description: Company description
        website: (Optional) Company website
        location: (Optional) Company location
        employee_count: (Optional) Number of employees

    Returns:
        McpCommonResponse with created company details
    """
    try:
        db = next(get_db())
        
        company_data = CompanyModel(
            company_name=company_name,
            industry=industry,
            description=description,
            website=website,
            location=location,
            employee_count=employee_count,
        )
        
        created_company = await CompanyService.create_company(company_data, db, None)
        return McpCommonResponse(
            message=f"Company '{company_name}' created successfully",
            success=True,
            data=created_company.dict() if hasattr(created_company, "dict") else created_company,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_companies() -> McpCommonResponse:
    """
    Retrieve a list of all companies.

    Returns:
        McpCommonResponse with list of companies
    """
    try:
        db = next(get_db())
        companies = await CompanyService.get_companies(db)
        return McpCommonResponse(
            message="Companies retrieved successfully",
            success=True,
            data=companies,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_company_by_id(company_id: str) -> McpCommonResponse:
    """
    Retrieve a specific company by its ID.

    Args:
        company_id: The ID of the company

    Returns:
        McpCommonResponse with company details
    """
    try:
        db = next(get_db())
        company = await CompanyService.get_company_by_id(company_id, db)
        if not company:
            return McpCommonResponse(
                message="Company not found", success=False
            )
        return McpCommonResponse(
            message="Company retrieved successfully",
            success=True,
            data=company.dict() if hasattr(company, "dict") else company,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def search_companies_by_name(company_name: str) -> McpCommonResponse:
    """
    Search for companies by name.

    Args:
        company_name: Company name to search for

    Returns:
        McpCommonResponse with matching companies
    """
    try:
        db = next(get_db())
        from app.models.company import Company
        
        companies = db.query(Company).filter(
            Company.company_name.ilike(f"%{company_name}%")
        ).all()
        
        if not companies:
            return McpCommonResponse(
                message="No companies found with that name", success=False
            )
        return McpCommonResponse(
            message="Companies found successfully",
            success=True,
            data=companies,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def search_companies_by_industry(industry: str) -> McpCommonResponse:
    """
    Search for companies by industry.

    Args:
        industry: Industry type to search for

    Returns:
        McpCommonResponse with matching companies
    """
    try:
        db = next(get_db())
        from app.models.company import Company
        
        companies = db.query(Company).filter(
            Company.industry.ilike(f"%{industry}%")
        ).all()
        
        if not companies:
            return McpCommonResponse(
                message="No companies found in that industry", success=False
            )
        return McpCommonResponse(
            message="Companies found successfully",
            success=True,
            data=companies,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def update_company(
    company_id: str,
    company_name: Optional[str] = None,
    industry: Optional[str] = None,
    description: Optional[str] = None,
    website: Optional[str] = None,
    location: Optional[str] = None,
    employee_count: Optional[str] = None,
) -> McpCommonResponse:
    """
    Update a company record.

    Args:
        company_id: ID of the company to update
        company_name: (Optional) Updated company name
        industry: (Optional) Updated industry
        description: (Optional) Updated description
        website: (Optional) Updated website
        location: (Optional) Updated location
        employee_count: (Optional) Updated employee count

    Returns:
        McpCommonResponse with updated company details
    """
    try:
        db = next(get_db())
        
        update_data = {}
        if company_name:
            update_data["company_name"] = company_name
        if industry:
            update_data["industry"] = industry
        if description:
            update_data["description"] = description
        if website:
            update_data["website"] = website
        if location:
            update_data["location"] = location
        if employee_count:
            update_data["employee_count"] = employee_count
        
        company_model = CompanyModel(**update_data) if update_data else None
        if not company_model:
            return McpCommonResponse(
                message="No fields to update", success=False
            )
        
        updated_company = await CompanyService.update_company(company_id, company_model, db)
        return McpCommonResponse(
            message="Company updated successfully",
            success=True,
            data=updated_company.dict() if hasattr(updated_company, "dict") else updated_company,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_company(company_id: str) -> McpCommonResponse:
    """
    Delete a company record.

    Args:
        company_id: ID of the company to delete

    Returns:
        McpCommonResponse with delete confirmation
    """
    try:
        db = next(get_db())
        response = await CompanyService.delete_company(company_id, db)
        return McpCommonResponse(
            message="Company deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
