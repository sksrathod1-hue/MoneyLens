from database.database import db

class Category(db.Model):
    __tablename__ = "categories"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True) # Null user_id means global system default
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'income' or 'expense'
    icon = db.Column(db.String(50), default="tag") # Icon identifier for UI
    color = db.Column(db.String(20), default="#ccc") # Hex code for color-coding
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    transactions = db.relationship("Transaction", backref="category", lazy=True)
    budgets = db.relationship("Budget", backref="category", cascade="all, delete-orphan", lazy=True)
    
    def to_dict(self):
        """Serialize the Category object to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "type": self.type,
            "icon": self.icon,
            "color": self.color,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
