import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from middleware.auth import token_required
from models.transaction import Transaction
from models.category import Category
from database.database import db
from utils.validators import validate_transaction_payload
from utils.helpers import parse_date_string, serialize_list

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("", methods=["GET"])
@token_required
def list_transactions(current_user):
    """Fetch user transactions, support category, date range and type filtering."""
    category_id = request.args.get("category_id", type=int)
    tx_type = request.args.get("type", type=str)
    limit = request.args.get("limit", default=50, type=int)
    
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if tx_type:
        query = query.filter_by(type=tx_type)
        
    transactions = query.order_by(Transaction.date.desc(), Transaction.id.desc()).limit(limit).all()
    return jsonify(serialize_list(transactions)), 200

@transactions_bp.route("", methods=["POST"])
@token_required
def create_transaction(current_user):
    """Creates a new transaction record."""
    data = request.get_json() or {}
    
    # Validation
    errors = validate_transaction_payload(data)
    if errors:
        return jsonify({"error": "Bad Request", "messages": errors}), 400
        
    # Check if category exists
    category = Category.query.filter_by(id=data["category_id"]).first()
    if not category:
        return jsonify({"error": "Bad Request", "message": "Category not found."}), 400
        
    try:
        new_tx = Transaction(
            user_id=current_user.id,
            category_id=data["category_id"],
            amount=data["amount"],
            type=data["type"],
            description=data.get("description", ""),
            date=parse_date_string(data["date"]),
            sms_sender=data.get("sms_sender"),
            receipt_image_path=data.get("receipt_image_path")
        )
        db.session.add(new_tx)
        db.session.commit()
        
        # Trigger update of relevant budgets asynchronously/inline
        from services.budget_service import BudgetService
        from models.budget import Budget
        
        # Find active budget for this category
        active_budget = Budget.query.filter(
            Budget.user_id == current_user.id,
            Budget.category_id == data["category_id"],
            Budget.start_date <= new_tx.date,
            Budget.end_date >= new_tx.date
        ).first()
        if active_budget:
            BudgetService.update_budget_spending(active_budget)
            
        return jsonify(new_tx.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Error", "message": str(e)}), 500

@transactions_bp.route("/<int:tx_id>", methods=["DELETE"])
@token_required
def delete_transaction(current_user, tx_id):
    """Deletes a transaction record and updates budget spending."""
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first()
    if not tx:
        return jsonify({"error": "Not Found", "message": "Transaction not found."}), 404
        
    try:
        category_id = tx.category_id
        tx_date = tx.date
        
        db.session.delete(tx)
        db.session.commit()
        
        # Update budget spending if budget exists
        from services.budget_service import BudgetService
        from models.budget import Budget
        active_budget = Budget.query.filter(
            Budget.user_id == current_user.id,
            Budget.category_id == category_id,
            Budget.start_date <= tx_date,
            Budget.end_date >= tx_date
        ).first()
        if active_budget:
            BudgetService.update_budget_spending(active_budget)
            
        return jsonify({"message": "Transaction deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Error", "message": str(e)}), 500

@transactions_bp.route("/upload-receipt", methods=["POST"])
@token_required
def upload_receipt(current_user):
    """Saves uploaded receipt file and returns local path."""
    if "receipt" not in request.files:
        return jsonify({"error": "Bad Request", "message": "No file uploaded."}), 400
        
    file = request.files["receipt"]
    if file.filename == "":
        return jsonify({"error": "Bad Request", "message": "Empty file name."}), 400
        
    if file:
        filename = secure_filename(f"user_{current_user.id}_{file.filename}")
        save_path = os.path.join(current_app.config["RECEIPT_UPLOAD_DIR"], filename)
        file.save(save_path)
        
        # Return path relative to project for DB storing
        relative_path = os.path.join("uploads", "receipts", filename)
        return jsonify({
            "message": "Receipt uploaded successfully.",
            "path": relative_path.replace("\\", "/") # standardize path separators
        }), 200
        
    return jsonify({"error": "Bad Request", "message": "File upload failed."}), 400
