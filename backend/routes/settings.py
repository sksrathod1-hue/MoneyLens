from flask import Blueprint, jsonify, request
from middleware.auth import token_required
from models.category import Category
from database.database import db
from services.category_service import CategoryService
from utils.helpers import serialize_list

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/categories", methods=["GET"])
@token_required
def get_categories(current_user):
    """Retrieve user categories (default and custom)."""
    categories = CategoryService.get_user_categories(current_user.id)
    return jsonify(serialize_list(categories)), 200

@settings_bp.route("/categories", methods=["POST"])
@token_required
def create_custom_category(current_user):
    """Create a new custom category for current user."""
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    cat_type = data.get("type", "expense").strip() # 'income' or 'expense'
    icon = data.get("icon", "tag").strip()
    color = data.get("color", "#95a5a6").strip()
    
    if not name or cat_type not in ["income", "expense"]:
        return jsonify({"error": "Bad Request", "message": "name and valid type are required."}), 400
        
    # Check if category already exists for user
    existing = Category.query.filter_by(user_id=current_user.id, name=name).first()
    if existing:
        return jsonify({"error": "Conflict", "message": "Category name already exists."}), 409
        
    try:
        new_cat = CategoryService.create_category(
            user_id=current_user.id,
            name=name,
            cat_type=cat_type,
            icon=icon,
            color=color
        )
        return jsonify(new_cat.to_dict()), 201
    except Exception as e:
        return jsonify({"error": "Internal Error", "message": str(e)}), 500
