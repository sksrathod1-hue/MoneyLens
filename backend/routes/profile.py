from flask import Blueprint, jsonify, request
from middleware.auth import token_required
from models.transaction import Transaction
from models.budget import Budget
from database.database import db

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("", methods=["GET"])
@token_required
def get_profile(current_user):
    """Retrieve logged-in user profile with statistics."""
    tx_count = Transaction.query.filter_by(user_id=current_user.id).count()
    budget_count = Budget.query.filter_by(user_id=current_user.id).count()
    
    user_dict = current_user.to_dict()
    user_dict["stats"] = {
        "total_transactions": tx_count,
        "total_budgets": budget_count
    }
    
    return jsonify(user_dict), 200

@profile_bp.route("", methods=["PUT"])
@token_required
def update_profile(current_user):
    """Update profile email."""
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    
    if not email:
        return jsonify({"error": "Bad Request", "message": "Email is required."}), 400
        
    # Check duplicate email
    existing = db.session.query(db.func.count(User.id)).filter(
        User.email == email, 
        User.id != current_user.id
    ).scalar()
    
    # Wait, User isn't imported from models in this file yet. Let's import it first
    from models.user import User
    existing = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing:
        return jsonify({"error": "Conflict", "message": "Email already in use by another account."}), 409
        
    try:
        current_user.email = email
        db.session.commit()
        return jsonify({
            "message": "Profile updated successfully.",
            "user": current_user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Error", "message": str(e)}), 500
