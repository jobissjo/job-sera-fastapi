from . import mcp
from app.services.notification_service import NotificationService
from app.core.database import get_db
from app.schema.common import McpCommonResponse
from typing import Optional


@mcp.tool
async def create_notification(
    user_id: str,
    title: str,
    message: str,
    notification_type: str,
    related_resource_id: Optional[str] = None,
) -> McpCommonResponse:
    """
    Create a new notification for a user.

    Args:
        user_id: ID of the user receiving the notification
        title: Notification title
        message: Notification message
        notification_type: Type of notification (e.g., 'job_match', 'application_status', 'message')
        related_resource_id: (Optional) ID of related resource (job, application, etc.)

    Returns:
        McpCommonResponse with notification details
    """
    try:
        db = next(get_db())
        
        notification = await NotificationService.create_notification(
            user_id, title, message, notification_type, related_resource_id, db
        )
        
        return McpCommonResponse(
            message="Notification created successfully",
            success=True,
            data=notification.dict() if hasattr(notification, "dict") else notification,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_notification_by_id(notification_id: str) -> McpCommonResponse:
    """
    Retrieve a notification by ID.

    Args:
        notification_id: The ID of the notification

    Returns:
        McpCommonResponse with notification details
    """
    try:
        db = next(get_db())
        
        notification = await NotificationService.get_notification_by_id(notification_id, db)
        
        if not notification:
            return McpCommonResponse(
                message="Notification not found", success=False
            )
        
        return McpCommonResponse(
            message="Notification retrieved successfully",
            success=True,
            data=notification.dict() if hasattr(notification, "dict") else notification,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def get_user_notifications(
    user_id: str,
    unread_only: bool = False,
) -> McpCommonResponse:
    """
    Retrieve all notifications for a user.

    Args:
        user_id: ID of the user
        unread_only: If True, return only unread notifications

    Returns:
        McpCommonResponse with list of notifications
    """
    try:
        db = next(get_db())
        
        notifications = await NotificationService.get_user_notifications(
            user_id, unread_only, db
        )
        
        if not notifications:
            return McpCommonResponse(
                message="No notifications found", success=False
            )
        
        return McpCommonResponse(
            message="Notifications retrieved successfully",
            success=True,
            data=notifications,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def mark_notification_as_read(notification_id: str) -> McpCommonResponse:
    """
    Mark a notification as read.

    Args:
        notification_id: ID of the notification

    Returns:
        McpCommonResponse with updated notification
    """
    try:
        db = next(get_db())
        
        notification = await NotificationService.mark_as_read(notification_id, db)
        
        return McpCommonResponse(
            message="Notification marked as read",
            success=True,
            data=notification.dict() if hasattr(notification, "dict") else notification,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def mark_all_notifications_as_read(user_id: str) -> McpCommonResponse:
    """
    Mark all notifications for a user as read.

    Args:
        user_id: ID of the user

    Returns:
        McpCommonResponse with confirmation
    """
    try:
        db = next(get_db())
        
        response = await NotificationService.mark_all_as_read(user_id, db)
        
        return McpCommonResponse(
            message="All notifications marked as read",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_notification(notification_id: str) -> McpCommonResponse:
    """
    Delete a notification.

    Args:
        notification_id: ID of the notification to delete

    Returns:
        McpCommonResponse with delete confirmation
    """
    try:
        db = next(get_db())
        
        response = await NotificationService.delete_notification(notification_id, db)
        
        return McpCommonResponse(
            message="Notification deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)


@mcp.tool
async def delete_all_notifications(user_id: str) -> McpCommonResponse:
    """
    Delete all notifications for a user.

    Args:
        user_id: ID of the user

    Returns:
        McpCommonResponse with confirmation
    """
    try:
        db = next(get_db())
        
        response = await NotificationService.delete_all_notifications(user_id, db)
        
        return McpCommonResponse(
            message="All notifications deleted successfully",
            success=True,
            data=response,
        )
    except Exception as e:
        return McpCommonResponse(message=str(e), success=False)
