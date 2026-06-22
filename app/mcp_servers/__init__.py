from mcp.server.fastmcp import FastMCP

mcp = FastMCP("jobsera-mcp-server", "0.1.0")

# Import all MCP server modules
from . import users
from . import jobs
from . import employers
from . import companies
from . import job_applications
from . import saved_jobs
from . import user_profiles
from . import user_notifications

