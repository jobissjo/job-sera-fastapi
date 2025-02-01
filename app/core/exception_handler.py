from app.core.logger import logger
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def http_exception_handler(request:Request, exc:HTTPException):
    logger.error(f"HTTP exception: {exc.detail} - status code: {exc.status_code} - - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(request:Request, exc:RequestValidationError):
    logger.warning(f"ValidationError: {exc.errors()} - Body: {exc.body} - Path: {request.url.path}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )



async def global_exception_handler(request:Request, exc:Exception):
    logger.critical(f"Unhandled Exception: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )
