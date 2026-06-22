from . import mcp
from app.schema.employer import EmployerProfileType, PersonalInformation, CompanyInformation, AdditionalInformation, Address
from app.services.employer_service import EmployerService
from app.core.database import get_db
from app.schema.common import McpCommonResponse
from typing import Optional


@mcp.tool
async def create_employer(
    employer_id: str,
    first_name: str,
    last_name: str,
    username: str,
    email: str,
    phone_number: str,
    position: str,
    social_media_link: str,
    gender: str,
    company_name: str,
    industry: str,
    company_size: str,
    business_type: str,
    company_phone: str,
    company_website: str,
    company_social_media: str,
    company_desc: str,
    street: str,
    city: str,
    landmark: str,
    state: str,
    country: str,
    postal_code: str,
    hear_about_us: str,
    agreed_to_terms: bool,
) -> McpCommonResponse:
    """
    Create a new employer profile.

    Args:
        employer_id: Employer's user ID
        first_name: First name
        last_name: Last name
        username: Username
        email: Email address
        phone_number: Phone number
        position: Job position
        social_media_link: Social media profile link
        gender: Gender
        company_name: Company name
        industry: Industry type
        company_size: Company size
        business_type: Type of business
        company_phone: Company phone number
        company_website: Company website
        company_social_media: Company social media link
        company_desc: Company description
        street: Street address
        city: City
        landmark: Landmark
        state: State
        country: Country
        postal_code: Postal code
        hear_about_us: How they heard about the platform
        agreed_to_terms: Whether they agreed to terms

    Returns:
        McpCommonResponse with created employer profile
    """
    try:
        db = next(get_db())
        
        address = Address(
            street=street,
            city=city,
            landmark=landmark,
            state=state,
            country=country,
            postalCode=postal_code,
        )
        
        personal_info = PersonalInformation(
            firstName=first_name,
            lastName=last_name,
            username=username,
            email=email,
            phoneNumber=phone_number,
            position=position,
            socialMediaLink=social_media_link,
            gender=gender,
        )
        
        company_info = CompanyInformation(
            companyName=company_name,
            industry=industry,
            companySize=company_size,
            businessType=business_type,
            companyPhoneNumber=company_phone,
            companyWebsite=company_website,
            socialMediaLink=company_social_media,
            desc=company_desc,
            address=address,
        )
        
        additional_info = AdditionalInformation(
            hearAboutUs=hear_about_us,
            agreedToTerms=agreed_to_terms,
        )
        
        employer_profile = EmployerProfileType(
            employer_id=employer_id,
            personalInformation=personal_info,
            companyInformation=company_info,
            additionalInformation=additional_info,
        )
        
        created_employer = await EmployerService.create_employer(employer_profile, None, db)
        return McpCommonResponse(
            message=f"Employer profile for {company_name} created successfully",
            success=True,
            data=created_employer.dict() if hasattr(created_employer, "dict") else created_employer,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_employer_by_id(employer_id: str) -> McpCommonResponse:
    """
    Retrieve an employer profile by ID.

    Args:
        employer_id: The ID of the employer

    Returns:
        McpCommonResponse with employer profile details
    """
    try:
        db = next(get_db())
        employer_profile = await EmployerService.get_by_id(employer_id, db)
        if not employer_profile:
            return McpCommonResponse(
                message="Employer profile not found", success=False
            )
        return McpCommonResponse(
            message="Employer profile retrieved successfully",
            success=True,
            data=employer_profile.dict() if hasattr(employer_profile, "dict") else employer_profile,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def search_employers_by_name(company_name: str) -> McpCommonResponse:
    """
    Search for employers by company name.

    Args:
        company_name: Company name to search for

    Returns:
        McpCommonResponse with matching employer profiles
    """
    try:
        db = next(get_db())
        from app.models.employer import Employer
        
        employers = db.query(Employer).filter(
            Employer.companyName.ilike(f"%{company_name}%")
        ).all()
        
        if not employers:
            return McpCommonResponse(
                message="No employers found with that company name", success=False
            )
        return McpCommonResponse(
            message="Employers found successfully",
            success=True,
            data=employers,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def update_employer(
    employer_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    position: Optional[str] = None,
    company_name: Optional[str] = None,
    industry: Optional[str] = None,
    company_size: Optional[str] = None,
    company_website: Optional[str] = None,
) -> McpCommonResponse:
    """
    Update an employer profile.

    Args:
        employer_id: ID of the employer to update
        first_name: (Optional) Updated first name
        last_name: (Optional) Updated last name
        position: (Optional) Updated position
        company_name: (Optional) Updated company name
        industry: (Optional) Updated industry
        company_size: (Optional) Updated company size
        company_website: (Optional) Updated company website

    Returns:
        McpCommonResponse with updated employer profile
    """
    try:
        db = next(get_db())
        
        # Get existing employer
        employer = await EmployerService.get_by_id(employer_id, db)
        if not employer:
            return McpCommonResponse(
                message="Employer not found", success=False
            )
        
        # Update fields as needed
        update_data = {}
        if first_name:
            update_data["firstName"] = first_name
        if last_name:
            update_data["lastName"] = last_name
        if position:
            update_data["position"] = position
        if company_name:
            update_data["companyName"] = company_name
        if industry:
            update_data["industry"] = industry
        if company_size:
            update_data["companySize"] = company_size
        if company_website:
            update_data["companyWebsite"] = company_website
        
        updated_employer = await EmployerService.update_employer(employer_id, employer, db)
        return McpCommonResponse(
            message="Employer profile updated successfully",
            success=True,
            data=updated_employer.dict() if hasattr(updated_employer, "dict") else updated_employer,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_employer(employer_id: str) -> McpCommonResponse:
    """
    Delete an employer profile.

    Args:
        employer_id: ID of the employer to delete

    Returns:
        McpCommonResponse with delete confirmation
    """
    try:
        db = next(get_db())
        response = await EmployerService.delete_employer(employer_id, db)
        return McpCommonResponse(
            message="Employer profile deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
