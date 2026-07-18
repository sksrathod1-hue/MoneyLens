import re
from datetime import datetime

class SMSParserService:
    """Service to parse financial transaction SMS notifications."""
    
    # Regex patterns for debited/expense messages
    DEBIT_PATTERNS = [
        r"(?:debited|spent|paid)\s+(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)\s+at\s+([^.]+)",
        r"(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)\s+(?:debited|spent|withdrawn)\s+(?:for|from)\s+([^.]+)",
        r"transaction\s+of\s+(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)\s+done\s+at\s+([^.]+)"
    ]
    
    # Regex patterns for credited/income messages
    CREDIT_PATTERNS = [
        r"(?:credited|deposited|received)\s+(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)\s+(?:from|into)\s+([^.]+)",
        r"(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)\s+(?:credited|deposited)\s+to\s+([^.]+)"
    ]
    
    @classmethod
    def parse_sms(cls, sender: str, body: str) -> dict:
        """
        Parses SMS body and extracts transaction details.
        
        Returns:
            dict: {
                "amount": float or None,
                "type": 'income' | 'expense' or None,
                "description": str or None,
                "sms_sender": str
            }
        """
        body_clean = body.strip()
        
        # 1. Try debits
        for pattern in cls.DEBIT_PATTERNS:
            match = re.search(pattern, body_clean, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(",", "")
                merchant = match.group(2).strip()
                return {
                    "amount": float(amount_str),
                    "type": "expense",
                    "description": f"SMS Purchase at {merchant}",
                    "sms_sender": sender
                }
                
        # 2. Try credits
        for pattern in cls.CREDIT_PATTERNS:
            match = re.search(pattern, body_clean, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(",", "")
                source = match.group(2).strip()
                return {
                    "amount": float(amount_str),
                    "type": "income",
                    "description": f"SMS Credit from {source}",
                    "sms_sender": sender
                }
                
        # 3. Fallback: Check if there's any currency amount in text
        currency_match = re.search(r"(?:Rs\.?|INR)\s*([\d,]+(?:\.\d{2})?)", body_clean, re.IGNORECASE)
        if currency_match:
            amount_str = currency_match.group(1).replace(",", "")
            # Guessing type
            tx_type = "expense"
            if "credit" in body_clean.lower() or "received" in body_clean.lower() or "deposit" in body_clean.lower():
                tx_type = "income"
            return {
                "amount": float(amount_str),
                "type": tx_type,
                "description": f"SMS parsed transaction: {body_clean[:30]}...",
                "sms_sender": sender
            }
            
        return {
            "amount": None,
            "type": None,
            "description": None,
            "sms_sender": sender
        }
