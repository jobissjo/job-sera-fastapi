from . import mcp
from app.schema.jobs import CreateJobModel, ResponseJobModel
from app.services import JobService
from app.core.database import get_db
from app.schema.common import McpCommonResponse
from typing import Optional, List


@mcp.tool
async def create_job(
    job_title: str,
    company: str,
    location: str,
    description: str,
    salary: str,
    shift: str,
    job_type: str,
    experience: str,
    qualifications: List[str],
    responsibilities: List[str],
    skills: List[str],
    employer_id: str,
) -> McpCommonResponse:
    """
    Create a new job posting in the system.

    Args:
        job_title: Title of the job position
        company: Company name
        location: Job location
        description: Job description
        salary: Salary range
        shift: Shift type (e.g., full-time, part-time)
        job_type: Type of job
        experience: Required experience level
        qualifications: List of qualifications
        responsibilities: List of responsibilities
        skills: Required skills
        employer_id: ID of the employer creating the job

    Returns:
        McpCommonResponse with success message and job details
    """
    try:
        db = next(get_db())
        job_data = CreateJobModel(
            jobTitle=job_title,
            company=company,
            location=location,
            description=description,
            salary=salary,
            shift=shift,
            jobType=job_type,
            experience=experience,
            qualifications=qualifications,
            responsibilities=responsibilities,
            skills=skills,
            employerId=employer_id,
        )
        created_job = await JobService.create_job(job_data, db)
        return McpCommonResponse(
            message=f"Job '{job_title}' created successfully",
            success=True,
            data=created_job.dict() if hasattr(created_job, "dict") else created_job,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_jobs(page_size: int = 10, page_number: int = 1) -> McpCommonResponse:
    """
    Retrieve a list of all jobs with pagination.

    Args:
        page_size: Number of jobs per page
        page_number: Page number to retrieve

    Returns:
        McpCommonResponse with list of jobs
    """
    try:
        db = next(get_db())
        jobs = await JobService.get_jobs(db, page_size, page_number)
        return McpCommonResponse(
            message="Jobs retrieved successfully",
            success=True,
            data=jobs,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_job_by_id(job_id: str) -> McpCommonResponse:
    """
    Retrieve a specific job by its ID.

    Args:
        job_id: The ID of the job to retrieve

    Returns:
        McpCommonResponse with job details
    """
    try:
        db = next(get_db())
        job = await JobService.get_job_by_id(job_id, db)
        if not job:
            return McpCommonResponse(
                message="Job not found", success=False
            )
        return McpCommonResponse(
            message="Job retrieved successfully",
            success=True,
            data=job.dict() if hasattr(job, "dict") else job,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def search_jobs_by_name(
    job_title: str,
    location: Optional[str] = None,
    experience: Optional[str] = None,
) -> McpCommonResponse:
    """
    Search for jobs by title, location, and experience level.

    Args:
        job_title: Job title to search for
        location: (Optional) Job location to filter
        experience: (Optional) Experience level to filter

    Returns:
        McpCommonResponse with matching jobs
    """
    try:
        db = next(get_db())
        jobs = await JobService.search_jobs(job_title, location, experience, db)
        return McpCommonResponse(
            message="Jobs found successfully",
            success=True,
            data=jobs,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_jobs_by_employer(employer_id: str) -> McpCommonResponse:
    """
    Retrieve all jobs posted by a specific employer.

    Args:
        employer_id: The ID of the employer

    Returns:
        McpCommonResponse with list of jobs by employer
    """
    try:
        db = next(get_db())
        from app.models.jobs import Job

        jobs = db.query(Job).filter(Job.employerId == employer_id).all()
        if not jobs:
            return McpCommonResponse(
                message="No jobs found for this employer", success=False
            )
        return McpCommonResponse(
            message="Jobs retrieved successfully",
            success=True,
            data=jobs,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def update_job(
    job_id: str,
    job_title: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    description: Optional[str] = None,
    salary: Optional[str] = None,
    shift: Optional[str] = None,
    job_type: Optional[str] = None,
    experience: Optional[str] = None,
    qualifications: Optional[List[str]] = None,
    responsibilities: Optional[List[str]] = None,
    skills: Optional[List[str]] = None,
) -> McpCommonResponse:
    """
    Update a job posting.

    Args:
        job_id: ID of the job to update
        job_title: (Optional) Updated job title
        company: (Optional) Updated company name
        location: (Optional) Updated location
        description: (Optional) Updated description
        salary: (Optional) Updated salary
        shift: (Optional) Updated shift type
        job_type: (Optional) Updated job type
        experience: (Optional) Updated experience requirement
        qualifications: (Optional) Updated qualifications list
        responsibilities: (Optional) Updated responsibilities list
        skills: (Optional) Updated skills list

    Returns:
        McpCommonResponse with updated job details
    """
    try:
        db = next(get_db())
        update_data = {}
        if job_title:
            update_data["jobTitle"] = job_title
        if company:
            update_data["company"] = company
        if location:
            update_data["location"] = location
        if description:
            update_data["description"] = description
        if salary:
            update_data["salary"] = salary
        if shift:
            update_data["shift"] = shift
        if job_type:
            update_data["jobType"] = job_type
        if experience:
            update_data["experience"] = experience
        if qualifications:
            update_data["qualifications"] = qualifications
        if responsibilities:
            update_data["responsibilities"] = responsibilities
        if skills:
            update_data["skills"] = skills

        job_model = ResponseJobModel(**update_data, id=job_id) if update_data else None
        if not job_model:
            return McpCommonResponse(
                message="No fields to update", success=False
            )

        error_message, response = await JobService.update_job(job_id, job_model, db, None)
        if error_message:
            return McpCommonResponse(message=error_message, success=False)
        return McpCommonResponse(
            message="Job updated successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_job(job_id: str) -> McpCommonResponse:
    """
    Delete a job posting.

    Args:
        job_id: ID of the job to delete

    Returns:
        McpCommonResponse with delete confirmation
    """
    try:
        db = next(get_db())
        error_message, response = await JobService.delete_job(job_id, db, None)
        if error_message:
            return McpCommonResponse(message=error_message, success=False)
        return McpCommonResponse(
            message="Job deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
