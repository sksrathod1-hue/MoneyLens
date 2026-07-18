from models.notification import Notification
from database.database import db

class NotificationService:
    """Service to create, read, and dispatch notifications to users."""
    
    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False):
        """Fetch notifications for a user."""
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(Notification.created_at.desc()).all()
        
    @staticmethod
    def create_notification(user_id: int, title: str, message: str, notif_type: str = "info"):
        """Create a notification in database."""
        # Simple duplicate checker to avoid flooding budget alerts
        existing = Notification.query.filter_by(
            user_id=user_id, 
            title=title, 
            message=message, 
            is_read=False
        ).first()
        if existing:
            return existing
            
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notif_type,
            is_read=False
        )
        db.session.add(notif)
        db.session.commit()
        return notif
        
    @staticmethod
    def mark_as_read(notification_id: int, user_id: int):
        """Mark a notification as read."""
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            db.session.commit()
            return True
        return False
        
    @staticmethod
    def mark_all_as_read(user_id: int):
        """Mark all notifications as read for a user."""
        Notification.query.filter_by(user_id=user_id, is_read=False).update({Notification.is_read: True})
        db.session.commit()
        return True
