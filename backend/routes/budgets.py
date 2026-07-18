from flask import Blueprint, request, jsonify
from middleware.auth import token_required
from models.budget import Budget
from models.category import Category
from services.budget_service import BudgetService
from database.database import db
from utils.helpers import parse_date_string, serialize_list

budgets_bp = Blueprint("budgets", __name__)

@budgets_bp.route("", methods=["GET"])
@token_required
def list_budgets(current_user):
    """List budgets for current user."""
    budgets = BudgetService.get_user_budgets(current_user.id)
    return jsonify(serialize_list(budgets)), 200

@budgets_bp.route("", methods=["POST"])
@token_required
def create_budget(current_user):
    """Create a new budget limit for a category."""
    data = request.get_json() or {}
    category_id = data.get("category_id")
    amount = data.get("amount")
    period = data.get("period", "monthly")
    start_str = data.get("start_date")
    end_str = data.get("end_date")
    
    if not category_id or not amount or not start_str or not end_str:
        return jsonify({"error": "Bad Request", "message": "category_id, amount, start_date and end_date are required."}), 400
        
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return jsonify({"error": "Bad Request", "message": "Category not found."}), 400
        
    try:
        start_date = parse_date_string(start_str)
        end_date = parse_date_string(end_str)
        
        # Check if budget already exists for this category and date overlap
        existing = Budget.query.filter(
            Budget.user_id == current_user.id,
            Budget.category_id == category_id,
            Budget.start_date <= end_date,
            Budget.end_date >= start_date
        ).first()
        
        if existing:
            return jsonify({
                "error": "Conflict", 
                "message": "A budget already exists for this category within the selected period."
            }), 409
            
        budget = BudgetService.create_budget(
            user_id=current_user.id,
            category_id=category_id,
            amount=float(amount),
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        return jsonify(budget.to_dict()), 201
    except Exception as e:
        return jsonify({"error": "Internal Error", "message": str(e)}), 500

@budgets_bp.route("/<int:budget_id>", methods=["DELETE"])
@token_required
def delete_budget(current_user, budget_id):
    """Remove a budget constraint."""
    budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first()
    if not budget:
        return jsonify({"error": "Not Found", "message": "Budget not found."}), 404
        
    try:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({"message": "Budget deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Error", "message": str(e)}), 500
