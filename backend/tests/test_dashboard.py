import pytest
import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database.database import db
from models.user import User
from models.category import Category
from models.transaction import Transaction

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "test-jwt-secret"
    SECRET_KEY = "test-secret"
    RECEIPT_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "test_receipts"))
    STATEMENT_UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads", "test_statements"))

@pytest.fixture
def test_setup():
    """Setup app client, database, user, and helper entities."""
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Register user
            reg_payload = {
                "username": "dashboard_test",
                "email": "dash@test.com",
                "password": "mypassword100"
            }
            client.post("/api/auth/register", json=reg_payload)
            
            # Login
            login_resp = client.post("/api/auth/login", json={
                "username": "dashboard_test",
                "password": "mypassword100"
            })
            token = login_resp.get_json()["access_token"]
            
            user = User.query.filter_by(username="dashboard_test").first()
            salary_cat = Category.query.filter_by(name="Salary").first()
            rent_cat = Category.query.filter_by(name="Rent & Housing").first()
            
            yield client, {"Authorization": f"Bearer {token}"}, user.id, salary_cat.id, rent_cat.id
            
            db.session.remove()
            db.drop_all()

def test_dashboard_summary_empty(test_setup):
    """Test dashboard calculations when user has no transactions yet."""
    client, headers, user_id, _, _ = test_setup
    
    response = client.get("/api/dashboard/summary", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["metrics"]["monthly_income"] == 0.0
    assert data["metrics"]["monthly_expense"] == 0.0
    assert data["metrics"]["net_savings"] == 0.0
    assert len(data["recent_transactions"]) == 0

def test_dashboard_summary_populated(test_setup):
    """Test dashboard income/expense sums and limits."""
    client, headers, user_id, sal_id, rent_id = test_setup
    today = datetime.date.today()
    
    # Add income
    tx1 = Transaction(user_id=user_id, category_id=sal_id, amount=3000.00, type="income", date=today)
    # Add expenses
    tx2 = Transaction(user_id=user_id, category_id=rent_id, amount=1200.00, type="expense", date=today)
    tx3 = Transaction(user_id=user_id, category_id=rent_id, amount=50.00, type="expense", date=today)
    db.session.add_all([tx1, tx2, tx3])
    db.session.commit()
    
    response = client.get("/api/dashboard/summary", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["metrics"]["monthly_income"] == 3000.00
    assert data["metrics"]["monthly_expense"] == 1250.00
    assert data["metrics"]["net_savings"] == 1750.00
    assert len(data["recent_transactions"]) == 3
