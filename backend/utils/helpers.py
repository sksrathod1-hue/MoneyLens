import datetime
from decimal import Decimal

def serialize_list(model_list):
    """Utility to convert a list of SQLAlchemy model instances into dictionary representations."""
    return [item.to_dict() for item in model_list]

def format_currency(value):
    """Format float or decimal as clean currency string."""
    if value is None:
        return "$0.00"
    try:
        val = float(value)
        return f"${val:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def parse_date_string(date_str):
    """Parse date from ISO string (YYYY-MM-DD) or fallback to today."""
    if not date_str:
        return datetime.date.today()
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return datetime.date.today()
