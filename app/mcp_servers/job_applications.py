from . import mcp
from app.services.job_application_service import JobApplicationService
from app.core.database import get_db
from app.schema.common import McpCommonResponse
from typing import Optional


@mcp.tool
async def create_job_application(
    job_id: str,
    user_id: str,
    resume_path: Optional[str] = None,
    cover_letter: Optional[str] = None,
) -> McpCommonResponse:
    """
    Create a new job application for a user.

    Args:
        job_id: ID of the job being applied for
        user_id: ID of the user applying
        resume_path: (Optional) Path to the uploaded resume
        cover_letter: (Optional) Cover letter text

    Returns:
        McpCommonResponse with application details
    """
    try:
        db = next(get_db())
        
        application = await JobApplicationService.create_application(
            job_id, user_id, resume_path, cover_letter, db
        )
        
        return McpCommonResponse(
            message="Job application submitted successfully",
            success=True,
            data=application.dict() if hasattr(application, "dict") else application,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_application_by_id(application_id: str) -> McpCommonResponse:
    """
    Retrieve a job application by ID.

    Args:
        application_id: The ID of the application

    Returns:
        McpCommonResponse with application details
    """
    try:
        db = next(get_db())
        
        application = await JobApplicationService.get_application_by_id(application_id, db)
        
        if not application:
            return McpCommonResponse(
                message="Application not found", success=False
            )
        
        return McpCommonResponse(
            message="Application retrieved successfully",
            success=True,
            data=application.dict() if hasattr(application, "dict") else application,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_applications_by_user(user_id: str) -> McpCommonResponse:
    """
    Retrieve all applications submitted by a specific user.

    Args:
        user_id: The ID of the user

    Returns:
        McpCommonResponse with list of user's applications
    """
    try:
        db = next(get_db())
        
        applications = await JobApplicationService.get_applications_by_user(user_id, db)
        
        if not applications:
            return McpCommonResponse(
                message="No applications found for this user", success=False
            )
        
        return McpCommonResponse(
            message="Applications retrieved successfully",
            success=True,
            data=applications,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_applications_by_job(job_id: str) -> McpCommonResponse:
    """
    Retrieve all applications for a specific job.

    Args:
        job_id: The ID of the job

    Returns:
        McpCommonResponse with list of applications for the job
    """
    try:
        db = next(get_db())
        
        applications = await JobApplicationService.get_applications_by_job(job_id, db)
        
        if not applications:
            return McpCommonResponse(
                message="No applications found for this job", success=False
            )
        
        return McpCommonResponse(
            message="Applications retrieved successfully",
            success=True,
            data=applications,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def update_application_status(
    application_id: str,
    status: str,
) -> McpCommonResponse:
    """
    Update the status of a job application.

    Args:
        application_id: ID of the application to update
        status: New status (e.g., 'pending', 'accepted', 'rejected', 'in_review')

    Returns:
        McpCommonResponse with updated application
    """
    try:
        db = next(get_db())
        
        updated_application = await JobApplicationService.update_application_status(
            application_id, status, db
        )
        
        return McpCommonResponse(
            message="Application status updated successfully",
            success=True,
            data=updated_application.dict() if hasattr(updated_application, "dict") else updated_application,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_application(application_id: str) -> McpCommonResponse:
    """
    Delete a job application.

    Args:
        application_id: ID of the application to delete

    Returns:
        McpCommonResponse with delete confirmation
    """
    try:
        db = next(get_db())
        
        response = await JobApplicationService.delete_application(application_id, db)
        
        return McpCommonResponse(
            message="Application deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
