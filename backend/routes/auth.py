from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database.database import db
from models.user import User
from utils.validators import validate_email, validate_password_strength

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    if not username or not email or not password:
        return jsonify({"error": "Bad Request", "message": "All fields are required."}), 400
        
    if not validate_email(email):
        return jsonify({"error": "Bad Request", "message": "Invalid email address format."}), 400
        
    is_strong, reason = validate_password_strength(password)
    if not is_strong:
        return jsonify({"error": "Bad Request", "message": reason}), 400
        
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Conflict", "message": "Username is already taken."}), 409
        
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Conflict", "message": "Email is already registered."}), 409
        
    try:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Automatically seed default categories for new user
        from models.category import Category
        default_categories = [
            {"name": "Salary", "type": "income", "icon": "briefcase", "color": "#2ecc71"},
            {"name": "Freelance", "type": "income", "icon": "laptop", "color": "#1abc9c"},
            {"name": "Food & Dining", "type": "expense", "icon": "coffee", "color": "#e67e22"},
            {"name": "Rent & Housing", "type": "expense", "icon": "home", "color": "#3498db"},
            {"name": "Utilities", "type": "expense", "icon": "bolt", "color": "#f1c40f"},
            {"name": "Transportation", "type": "expense", "icon": "car", "color": "#34495e"},
            {"name": "Groceries", "type": "expense", "icon": "shopping-cart", "color": "#27ae60"},
            {"name": "Shopping", "type": "expense", "icon": "shopping-bag", "color": "#d35400"}
        ]
        for cat in default_categories:
            db_cat = Category(
                user_id=new_user.id,
                name=cat["name"],
                type=cat["type"],
                icon=cat["icon"],
                color=cat["color"],
                is_default=True
            )
            db.session.add(db_cat)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": new_user.to_dict()
        }), 211
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Error", "message": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify({"error": "Bad Request", "message": "Username and password are required."}), 400
        
    user = User.query.filter((User.username == username) | (User.email == username)).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Unauthorized", "message": "Invalid username or password."}), 401
        
    # Generate JWT access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200
