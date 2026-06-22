from . import mcp
from app.services.saved_job_service import SavedJobService
from app.core.database import get_db
from app.schema.common import McpCommonResponse


@mcp.tool
async def save_job(user_id: str, job_id: str) -> McpCommonResponse:
    """
    Save a job to the user's saved jobs list.

    Args:
        user_id: ID of the user saving the job
        job_id: ID of the job to save

    Returns:
        McpCommonResponse with confirmation
    """
    try:
        db = next(get_db())
        
        saved_job = await SavedJobService.save_job(user_id, job_id, db)
        
        return McpCommonResponse(
            message="Job saved successfully",
            success=True,
            data=saved_job.dict() if hasattr(saved_job, "dict") else saved_job,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_saved_jobs(user_id: str) -> McpCommonResponse:
    """
    Retrieve all saved jobs for a user.

    Args:
        user_id: ID of the user

    Returns:
        McpCommonResponse with list of saved jobs
    """
    try:
        db = next(get_db())
        
        saved_jobs = await SavedJobService.get_saved_jobs(user_id, db)
        
        if not saved_jobs:
            return McpCommonResponse(
                message="No saved jobs found", success=False
            )
        
        return McpCommonResponse(
            message="Saved jobs retrieved successfully",
            success=True,
            data=saved_jobs,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_saved_job_by_id(saved_job_id: str) -> McpCommonResponse:
    """
    Retrieve a specific saved job record by ID.

    Args:
        saved_job_id: The ID of the saved job record

    Returns:
        McpCommonResponse with saved job details
    """
    try:
        db = next(get_db())
        
        saved_job = await SavedJobService.get_saved_job_by_id(saved_job_id, db)
        
        if not saved_job:
            return McpCommonResponse(
                message="Saved job not found", success=False
            )
        
        return McpCommonResponse(
            message="Saved job retrieved successfully",
            success=True,
            data=saved_job.dict() if hasattr(saved_job, "dict") else saved_job,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def check_job_saved(user_id: str, job_id: str) -> McpCommonResponse:
    """
    Check if a specific job is saved by a user.

    Args:
        user_id: ID of the user
        job_id: ID of the job

    Returns:
        McpCommonResponse with boolean result
    """
    try:
        db = next(get_db())
        
        is_saved = await SavedJobService.check_job_saved(user_id, job_id, db)
        
        return McpCommonResponse(
            message="Check completed successfully",
            success=True,
            data={"is_saved": is_saved},
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def unsave_job(user_id: str, job_id: str) -> McpCommonResponse:
    """
    Remove a job from the user's saved jobs list.

    Args:
        user_id: ID of the user
        job_id: ID of the job to unsave

    Returns:
        McpCommonResponse with confirmation
    """
    try:
        db = next(get_db())
        
        response = await SavedJobService.unsave_job(user_id, job_id, db)
        
        return McpCommonResponse(
            message="Job removed from saved list successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
