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
def auth_client():
    """Setup app client, database, and log in a demo user to get JWT headers."""
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Register user
            reg_payload = {
                "username": "tester",
                "email": "tester@domain.com",
                "password": "mypassword100"
            }
            client.post("/api/auth/register", json=reg_payload)
            
            # Login
            login_resp = client.post("/api/auth/login", json={
                "username": "tester",
                "password": "mypassword100"
            })
            token = login_resp.get_json()["access_token"]
            
            # Retrieve generated category ID (created in registration blueprints)
            cat = Category.query.filter_by(name="Food & Dining").first()
            
            yield client, {"Authorization": f"Bearer {token}"}, cat.id, cat.user_id
            
            db.session.remove()
            db.drop_all()

def test_create_transaction(auth_client):
    """Test creating a valid transaction."""
    client, headers, cat_id, user_id = auth_client
    
    payload = {
        "amount": 42.50,
        "type": "expense",
        "category_id": cat_id,
        "date": "2026-07-16",
        "description": "Weekly Pizza Lunch"
    }
    
    response = client.post("/api/transactions", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["amount"] == 42.50
    assert data["type"] == "expense"
    assert data["description"] == "Weekly Pizza Lunch"
    
    # Check in DB
    tx = Transaction.query.get(data["id"])
    assert tx is not None
    assert tx.amount == 42.50

def test_list_transactions(auth_client):
    """Test retrieving transactions and filtering."""
    client, headers, cat_id, user_id = auth_client
    
    # Create a couple transactions
    tx1 = Transaction(user_id=user_id, category_id=cat_id, amount=10.00, type="expense", date=datetime.date.today())
    tx2 = Transaction(user_id=user_id, category_id=cat_id, amount=100.00, type="income", date=datetime.date.today())
    db.session.add_all([tx1, tx2])
    db.session.commit()
    
    response = client.get("/api/transactions", headers=headers)
    assert response.status_code == 200
    txs = response.get_json()
    assert len(txs) == 2
    
    # Filter by expense type
    response_filter = client.get("/api/transactions?type=expense", headers=headers)
    assert response_filter.status_code == 200
    filtered_txs = response_filter.get_json()
    assert len(filtered_txs) == 1
    assert filtered_txs[0]["amount"] == 10.00
