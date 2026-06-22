from . import mcp
from app.services.profile_service import ProfileService
from app.core.database import get_db
from app.schema.common import McpCommonResponse
from typing import Optional, List


@mcp.tool
async def create_user_profile(
    user_id: str,
    first_name: str,
    last_name: str,
    bio: Optional[str] = None,
    profile_picture_path: Optional[str] = None,
    location: Optional[str] = None,
    phone_number: Optional[str] = None,
    skills: Optional[List[str]] = None,
) -> McpCommonResponse:
    """
    Create a new user profile.

    Args:
        user_id: ID of the user
        first_name: User's first name
        last_name: User's last name
        bio: (Optional) User biography
        profile_picture_path: (Optional) Path to profile picture
        location: (Optional) User location
        phone_number: (Optional) Phone number
        skills: (Optional) List of skills

    Returns:
        McpCommonResponse with created profile details
    """
    try:
        db = next(get_db())
        
        profile = await ProfileService.create_profile(
            user_id, first_name, last_name, bio, profile_picture_path, 
            location, phone_number, skills, db
        )
        
        return McpCommonResponse(
            message=f"Profile for {first_name} {last_name} created successfully",
            success=True,
            data=profile.dict() if hasattr(profile, "dict") else profile,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_profile_by_user_id(user_id: str) -> McpCommonResponse:
    """
    Retrieve a user profile by user ID.

    Args:
        user_id: ID of the user

    Returns:
        McpCommonResponse with profile details
    """
    try:
        db = next(get_db())
        
        profile = await ProfileService.get_profile_by_user_id(user_id, db)
        
        if not profile:
            return McpCommonResponse(
                message="Profile not found", success=False
            )
        
        return McpCommonResponse(
            message="Profile retrieved successfully",
            success=True,
            data=profile.dict() if hasattr(profile, "dict") else profile,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def search_profiles_by_name(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> McpCommonResponse:
    """
    Search for user profiles by name.

    Args:
        first_name: (Optional) First name to search for
        last_name: (Optional) Last name to search for

    Returns:
        McpCommonResponse with matching profiles
    """
    try:
        db = next(get_db())
        
        profiles = await ProfileService.search_profiles_by_name(first_name, last_name, db)
        
        if not profiles:
            return McpCommonResponse(
                message="No profiles found with that name", success=False
            )
        
        return McpCommonResponse(
            message="Profiles found successfully",
            success=True,
            data=profiles,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def search_profiles_by_skills(skills: List[str]) -> McpCommonResponse:
    """
    Search for user profiles by skills.

    Args:
        skills: List of skills to search for

    Returns:
        McpCommonResponse with matching profiles
    """
    try:
        db = next(get_db())
        
        profiles = await ProfileService.search_profiles_by_skills(skills, db)
        
        if not profiles:
            return McpCommonResponse(
                message="No profiles found with those skills", success=False
            )
        
        return McpCommonResponse(
            message="Profiles found successfully",
            success=True,
            data=profiles,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def update_user_profile(
    user_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    bio: Optional[str] = None,
    profile_picture_path: Optional[str] = None,
    location: Optional[str] = None,
    phone_number: Optional[str] = None,
    skills: Optional[List[str]] = None,
) -> McpCommonResponse:
    """
    Update a user profile.

    Args:
        user_id: ID of the user
        first_name: (Optional) Updated first name
        last_name: (Optional) Updated last name
        bio: (Optional) Updated bio
        profile_picture_path: (Optional) Updated profile picture path
        location: (Optional) Updated location
        phone_number: (Optional) Updated phone number
        skills: (Optional) Updated skills list

    Returns:
        McpCommonResponse with updated profile details
    """
    try:
        db = next(get_db())
        
        profile = await ProfileService.update_profile(
            user_id, first_name, last_name, bio, profile_picture_path,
            location, phone_number, skills, db
        )
        
        return McpCommonResponse(
            message="Profile updated successfully",
            success=True,
            data=profile.dict() if hasattr(profile, "dict") else profile,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_user_profile(user_id: str) -> McpCommonResponse:
    """
    Delete a user profile.

    Args:
        user_id: ID of the user

    Returns:
        McpCommonResponse with delete confirmation
    """
    try:
        db = next(get_db())
        
        response = await ProfileService.delete_profile(user_id, db)
        
        return McpCommonResponse(
            message="Profile deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
