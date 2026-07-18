# Period constraints
PERIOD_MONTHLY = "monthly"
PERIOD_WEEKLY = "weekly"
PERIOD_YEARLY = "yearly"
BUDGET_PERIODS = [PERIOD_MONTHLY, PERIOD_WEEKLY, PERIOD_YEARLY]

# Transaction Types
TYPE_INCOME = "income"
TYPE_EXPENSE = "expense"
TRANSACTION_TYPES = [TYPE_INCOME, TYPE_EXPENSE]

# Default icons & colors for standard category seeding
CATEGORY_DEFAULTS = {
    "Salary": {"icon": "briefcase", "color": "#2ecc71"},
    "Groceries": {"icon": "shopping-cart", "color": "#27ae60"},
    "Rent": {"icon": "home", "color": "#3498db"},
    "Utilities": {"icon": "bolt", "color": "#f1c40f"},
    "Food": {"icon": "coffee", "color": "#e67e22"},
    "Entertainment": {"icon": "film", "color": "#e74c3c"},
    "Other": {"icon": "tag", "color": "#95a5a6"}
}
