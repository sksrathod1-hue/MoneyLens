from database.database import db
import bcrypt

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    categories = db.relationship("Category", backref="user", cascade="all, delete-orphan", lazy=True)
    transactions = db.relationship("Transaction", backref="user", cascade="all, delete-orphan", lazy=True)
    budgets = db.relationship("Budget", backref="user", cascade="all, delete-orphan", lazy=True)
    notifications = db.relationship("Notification", backref="user", cascade="all, delete-orphan", lazy=True)
    ai_insights = db.relationship("AIInsight", backref="user", cascade="all, delete-orphan", lazy=True)
    
    def set_password(self, password):
        """Hashes the password and saves it to password_hash."""
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.password_hash = hashed.decode("utf-8")
        
    def check_password(self, password):
        """Checks if a password matches the stored hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))
        
    def to_dict(self):
        """Serialize the User object to a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
