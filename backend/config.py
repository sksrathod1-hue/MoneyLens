import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration settings for MoneyLens backend."""
    
    # Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-secret-key-12345!")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    PORT = int(os.getenv("PORT", 5000))
    
    # SQLAlchemy (Database) Settings
    # Defaulting to an SQLite database named moneylens.db in the backend folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(BASE_DIR, 'moneylens.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret-key-67890!")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_EXPIRY_HOURS", 24)))
    
    # Upload Directories
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    RECEIPT_UPLOAD_DIR = os.path.join(UPLOAD_FOLDER, "receipts")
    STATEMENT_UPLOAD_DIR = os.path.join(UPLOAD_FOLDER, "statements")
    
    # Max file upload size (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
    
    # SMS gateway validation key
    SMS_GATEWAY_API_KEY = os.getenv("SMS_GATEWAY_API_KEY", "sms-auth-key-xyz")
    
    # AI service provider configuration
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "gemini-1.5-flash")
