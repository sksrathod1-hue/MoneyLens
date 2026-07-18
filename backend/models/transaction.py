import datetime
from database.database import db

class Transaction(db.Model):
    __tablename__ = "transactions"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'income' or 'expense'
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    sms_sender = db.Column(db.String(50), nullable=True) # Set if parsed from SMS
    receipt_image_path = db.Column(db.Text, nullable=True) # Path to local receipt upload
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        """Serialize the Transaction object to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else "Uncategorized",
            "category_color": self.category.color if self.category else "#ccc",
            "category_icon": self.category.icon if self.category else "tag",
            "amount": float(self.amount),
            "type": self.type,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "sms_sender": self.sms_sender,
            "receipt_image_path": self.receipt_image_path,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
