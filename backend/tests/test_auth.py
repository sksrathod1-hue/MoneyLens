import pytest
import sys
import os

# Include backend path in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database.database import db
from models.user import User

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-jwt-secret"
    SECRET_KEY = "test-secret"
    RECEIPT_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "test_receipts"))
    STATEMENT_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "test_statements"))

@pytest.fixture
def client():
    """Setup app test client and in-memory DB context."""
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_health_check(client):
    """Test standard health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_user_registration(client):
    """Test user signup endpoint flow."""
    payload = {
        "username": "testuser",
        "email": "test@user.com",
        "password": "securepassword123"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 211
    
    # Check database
    user = User.query.filter_by(username="testuser").first()
    assert user is not None
    assert user.email == "test@user.com"

def test_user_registration_missing_fields(client):
    """Test registration failure on missing payload keys."""
    payload = {
        "username": "testuser",
        "email": ""
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400

def test_user_login(client):
    """Test token retrieval on login."""
    # 1. Register
    reg_payload = {
        "username": "tester",
        "email": "tester@domain.com",
        "password": "mypassword100"
    }
    client.post("/api/auth/register", json=reg_payload)
    
    # 2. Login
    login_payload = {
        "username": "tester",
        "password": "mypassword100"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["user"]["username"] == "tester"
