import datetime
from models.budget import Budget
from models.transaction import Transaction
from database.database import db
from services.notification_service import NotificationService

class BudgetService:
    """Service to manage user budgets and check spending limitations."""
    
    @staticmethod
    def get_user_budgets(user_id: int):
        """Get all budgets for a user and recalculate current spend."""
        budgets = Budget.query.filter_by(user_id=user_id).all()
        for budget in budgets:
            BudgetService.update_budget_spending(budget)
        return budgets
        
    @staticmethod
    def update_budget_spending(budget: Budget):
        """Recalculates the amount spent under a budget category for its date range."""
        # Query total expense transactions for this user, category, and date range
        total_spent = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == budget.user_id,
            Transaction.category_id == budget.category_id,
            Transaction.type == "expense",
            Transaction.date >= budget.start_date,
            Transaction.date <= budget.end_date
        ).scalar() or 0.00
        
        budget.spent = float(total_spent)
        db.session.commit()
        
        # Check alerts
        percent = (budget.spent / budget.amount) * 100 if budget.amount > 0 else 0
        if percent >= 100:
            NotificationService.create_notification(
                user_id=budget.user_id,
                title="Budget Exceeded!",
                message=f"You have spent ${budget.spent:.2f} of your ${budget.amount:.2f} budget for category '{budget.category.name if budget.category else 'Unknown'}'.",
                notif_type="budget_alert"
            )
        elif percent >= 80:
            NotificationService.create_notification(
                user_id=budget.user_id,
                title="Budget Warning (80% Reached)",
                message=f"You have spent ${budget.spent:.2f} of your ${budget.amount:.2f} budget for category '{budget.category.name if budget.category else 'Unknown'}'.",
                notif_type="budget_alert"
            )
            
    @staticmethod
    def create_budget(user_id: int, category_id: int, amount: float, period: str, start_date: datetime.date, end_date: datetime.date):
        """Create a new budget and initial spent calculation."""
        new_budget = Budget(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_budget)
        db.session.commit()
        BudgetService.update_budget_spending(new_budget)
        return new_budget
