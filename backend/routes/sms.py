from flask import Blueprint, request, jsonify, current_app
from database.database import db
from models.user import User
from models.transaction import Transaction
from services.sms_parser import SMSParserService
from services.category_service import CategoryService
from services.budget_service import BudgetService
from services.notification_service import NotificationService
from models.budget import Budget
import datetime

sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/webhook", methods=["POST"])
def sms_webhook():
    """
    Webhook endpoint to parse SMS sent by a gateway or background daemon.
    Requires header `X-SMS-Gateway-Key` to match config value.
    """
    api_key = request.headers.get("X-SMS-Gateway-Key")
    expected_key = current_app.config.get("SMS_GATEWAY_API_KEY")
    
    if not api_key or api_key != expected_key:
        return jsonify({"error": "Unauthorized", "message": "Invalid SMS gateway credential key."}), 401
        
    data = request.get_json() or {}
    sms_body = data.get("body")
    sms_sender = data.get("sender")
    username_or_id = data.get("user") # Can be username or integer user ID
    
    if not sms_body or not sms_sender or not username_or_id:
        return jsonify({"error": "Bad Request", "message": "body, sender, and user fields are required."}), 400
        
    # Find user
    if isinstance(username_or_id, int) or username_or_id.isdigit():
        user = User.query.get(int(username_or_id))
    else:
        user = User.query.filter_by(username=username_or_id).first()
        
    if not user:
        return jsonify({"error": "Not Found", "message": "Target user not found."}), 404
        
    # Parse SMS
    parsed = SMSParserService.parse_sms(sms_sender, sms_body)
    if not parsed["amount"]:
        return jsonify({
            "message": "SMS processed but no transaction recognized.",
            "parsed": parsed
        }), 200
        
    # Guess Category
    category = CategoryService.guess_category(user.id, parsed["description"], parsed["type"])
    
    try:
        # Create Transaction
        today = datetime.date.today()
        new_tx = Transaction(
            user_id=user.id,
            category_id=category.id if category else None,
            amount=parsed["amount"],
            type=parsed["type"],
            description=parsed["description"],
            date=today,
            sms_sender=parsed["sms_sender"]
        )
        db.session.add(new_tx)
        db.session.commit()
        
        # Create user notification
        notif_msg = f"Automatically logged {parsed['type']} of ${parsed['amount']:.2f} at {category.name if category else 'Uncategorized'} from SMS."
        NotificationService.create_notification(
            user_id=user.id,
            title="SMS Expense Logged",
            message=notif_msg,
            notif_type="info"
        )
        
        # Check and update budget
        if category:
            active_budget = Budget.query.filter(
                Budget.user_id == user.id,
                Budget.category_id == category.id,
                Budget.start_date <= today,
                Budget.end_date >= today
            ).first()
            if active_budget:
                BudgetService.update_budget_spending(active_budget)
                
        return jsonify({
            "message": "SMS transaction registered successfully.",
            "transaction": new_tx.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal Error", "message": str(e)}), 500
