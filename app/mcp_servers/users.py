from . import mcp
from app.schema.users import CreateUserModel
from app.services import UserService
from app.core.database import get_db
from app.schema.common import McpCommonResponse

@mcp.tool
async def create_user(data:CreateUserModel)->McpCommonResponse:
    """
    Create a new user in the system.

    Returns:
        dict: A dictionary containing the created user's information.
    """
    # Here you would typically call your UserService to create the user
    # For example:
    db = get_db()
    created_user = await UserService.register_user(data, db)
    
    return McpCommonResponse(
        message=f"User {created_user.username} created successfully",
        success=True
    )