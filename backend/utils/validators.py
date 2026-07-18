import re

def validate_email(email: str) -> bool:
    """Checks if an email is formatted correctly."""
    if not email:
        return False
    # Standard email regex
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.match(email_regex, email.strip()))

def validate_password_strength(password: str) -> tuple:
    """
    Checks user passwords.
    Returns:
        (bool, str): (is_strong, failure_reason)
    """
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
        
    return True, ""

def validate_transaction_payload(data: dict) -> list:
    """
    Validates input schema when posting a transaction.
    Returns:
        list: list of validation error strings, empty if payload is valid.
    """
    errors = []
    if "amount" not in data:
        errors.append("Amount is required.")
    else:
        try:
            amt = float(data["amount"])
            if amt <= 0:
                errors.append("Amount must be greater than zero.")
        except (ValueError, TypeError):
            errors.append("Amount must be a numeric value.")
            
    if "type" not in data or data["type"] not in ["income", "expense"]:
        errors.append("Type must be either 'income' or 'expense'.")
        
    if "category_id" not in data:
        errors.append("Category ID is required.")
        
    if "date" not in data:
        errors.append("Date is required.")
        
    return errors
