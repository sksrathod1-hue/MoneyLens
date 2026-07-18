from flask import Blueprint, jsonify, request
from middleware.auth import token_required
from services.report_service import ReportService
from utils.helpers import parse_date_string
import datetime

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/category-breakdown", methods=["GET"])
@token_required
def category_breakdown(current_user):
    """Returns category spending totals for a date range."""
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")
    
    today = datetime.date.today()
    # Default: last 30 days
    start_date = parse_date_string(start_str) if start_str else (today - datetime.timedelta(days=30))
    end_date = parse_date_string(end_str) if end_str else today
    
    breakdown = ReportService.get_spending_by_category(current_user.id, start_date, end_date)
    return jsonify(breakdown), 200

@reports_bp.route("/income-vs-expense", methods=["GET"])
@token_required
def income_vs_expense(current_user):
    """Returns total income vs expense for a date range."""
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")
    
    today = datetime.date.today()
    # Default: last 30 days
    start_date = parse_date_string(start_str) if start_str else (today - datetime.timedelta(days=30))
    end_date = parse_date_string(end_str) if end_str else today
    
    summary = ReportService.get_income_vs_expense(current_user.id, start_date, end_date)
    return jsonify(summary), 200

@reports_bp.route("/trends", methods=["GET"])
@token_required
def monthly_trends(current_user):
    """Returns monthly income/expense trends for the past 6 months."""
    months = request.args.get("months", default=6, type=int)
    trends = ReportService.get_monthly_trends(current_user.id, months)
    return jsonify(trends), 200
