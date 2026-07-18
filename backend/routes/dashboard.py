from flask import Blueprint, jsonify
import datetime
from middleware.auth import token_required
from models.transaction import Transaction
from models.budget import Budget
from models.notification import Notification
from services.ai_service import AIService
from utils.helpers import serialize_list

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/summary", methods=["GET"])
@token_required
def get_dashboard_summary(current_user):
    """Returns aggregated summary data for the main dashboard view."""
    today = datetime.date.today()
    start_of_month = today.replace(day=1)
    
    # 1. Total monthly income vs expense
    transactions_this_month = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_of_month,
        Transaction.date <= today
    ).all()
    
    monthly_income = sum(float(t.amount) for t in transactions_this_month if t.type == "income")
    monthly_expense = sum(float(t.amount) for t in transactions_this_month if t.type == "expense")
    net_savings = monthly_income - monthly_expense
    
    # 2. Recent transactions (Limit 5)
    recent_transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.date.desc(), Transaction.id.desc()).limit(5).all()
    
    # 3. Active Budgets (Limit 3)
    active_budgets = Budget.query.filter(
        Budget.user_id == current_user.id,
        Budget.start_date <= today,
        Budget.end_date >= today
    ).limit(3).all()
    
    # 4. Unread notifications count
    unread_notif_count = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()
    
    # 5. Top AI Insight
    ai_insights = AIService.get_user_insights(current_user.id)
    top_insight = ai_insights[0].to_dict() if ai_insights else None
    
    return jsonify({
        "metrics": {
            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,
            "net_savings": net_savings,
            "unread_notifications": unread_notif_count
        },
        "recent_transactions": serialize_list(recent_transactions),
        "budgets": serialize_list(active_budgets),
        "top_insight": top_insight
    }), 200
