from database.database import db
from models.transaction import Transaction
from models.category import Category
import datetime
from collections import defaultdict

class ReportService:
    """Service to compute financial analytical metrics and statistics for graphs."""
    
    @staticmethod
    def get_spending_by_category(user_id: int, start_date: datetime.date, end_date: datetime.date):
        """Returns spending totals broken down by categories for a specified date range."""
        results = db.session.query(
            Category.name, 
            Category.color, 
            db.func.sum(Transaction.amount)
        ).join(
            Transaction, Category.id == Transaction.category_id
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Category.name, Category.color).all()
        
        return [
            {"category": name, "color": color, "total": float(total)} 
            for name, color, total in results
        ]

    @staticmethod
    def get_income_vs_expense(user_id: int, start_date: datetime.date, end_date: datetime.date):
        """Returns total income vs total expense in a date range."""
        results = db.session.query(
            Transaction.type, 
            db.func.sum(Transaction.amount)
        ).filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).group_by(Transaction.type).all()
        
        data = {"income": 0.00, "expense": 0.00}
        for tx_type, total in results:
            data[tx_type] = float(total)
            
        return data

    @staticmethod
    def get_monthly_trends(user_id: int, months_back: int = 6):
        """Returns monthly aggregates for income and expenses over the past N months."""
        today = datetime.date.today()
        # Start date: N months ago, first day of that month
        start_date = today - datetime.timedelta(days=30 * months_back)
        start_date = start_date.replace(day=1)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= today
        ).order_by(Transaction.date.asc()).all()
        
        monthly_data = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        
        for tx in transactions:
            month_key = tx.date.strftime("%Y-%m") # e.g. "2026-07"
            monthly_data[month_key][tx.type] += float(tx.amount)
            
        # Format for charts (sorting chronologically)
        sorted_keys = sorted(monthly_data.keys())
        trends = []
        for key in sorted_keys:
            trends.append({
                "month": key,
                "income": monthly_data[key]["income"],
                "expense": monthly_data[key]["expense"]
            })
            
        return trends
