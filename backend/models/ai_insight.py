from database.database import db

class AIInsight(db.Model):
    __tablename__ = "ai_insights"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    insight = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="spending") # 'spending', 'saving', 'investment'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        """Serialize the AIInsight object to a dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "insight": self.insight,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
