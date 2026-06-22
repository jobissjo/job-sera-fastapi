from pydantic import BaseModel


class McpCommonResponse(BaseModel):
    success: bool
    message: str | None = None