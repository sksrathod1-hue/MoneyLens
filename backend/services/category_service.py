from models.category import Category
from database.database import db

class CategoryService:
    """Service to handle category operations, including auto-categorization."""
    
    @staticmethod
    def get_user_categories(user_id: int):
        """Get default and custom categories for a user."""
        return Category.query.filter(
            (Category.user_id == user_id) | (Category.user_id.is_(None))
        ).all()
        
    @staticmethod
    def create_category(user_id: int, name: str, cat_type: str, icon: str = "tag", color: str = "#ccc"):
        """Create a custom category for a user."""
        new_cat = Category(
            user_id=user_id,
            name=name,
            type=cat_type,
            icon=icon,
            color=color,
            is_default=False
        )
        db.session.add(new_cat)
        db.session.commit()
        return new_cat
        
    @staticmethod
    def guess_category(user_id: int, description: str, tx_type: str) -> Category:
        """
        Guess category based on description terms.
        Falls back to 'Groceries' / 'Food & Dining' for expenses, or 'Salary' for income.
        """
        categories = CategoryService.get_user_categories(user_id)
        desc_lower = description.lower()
        
        # Simple match keywords
        keyword_mappings = {
            "food": ["food", "dining", "restaurant", "cafe", "uber eats", "starbucks", "mcdonald", "swiggy", "zomato", "pizza", "burger"],
            "groceries": ["grocery", "groceries", "supermarket", "walmart", "target", "whole foods", "mart"],
            "rent & housing": ["rent", "landlord", "mortgage", "housing", "apartment"],
            "utilities": ["electricity", "electric", "power", "water", "gas", "wifi", "internet", "broadband", "mobile recharge"],
            "transportation": ["uber", "lyft", "taxi", "gas", "petrol", "fuel", "train", "metro", "bus", "parking"],
            "entertainment": ["netflix", "spotify", "hulu", "disney", "movie", "cinema", "show", "theater", "game", "steam"],
            "salary": ["salary", "payroll", "direct deposit", "wage"],
            "freelance": ["freelance", "upwork", "fiverr", "invoice payment", "project payment"],
            "investments": ["dividend", "stocks", "mutual fund", "crypto", "trading"]
        }
        
        for cat_name, keywords in keyword_mappings.items():
            if any(kw in desc_lower for kw in keywords):
                # Find category object in database list
                matched_cat = next((c for c in categories if c.name.lower() == cat_name), None)
                if matched_cat and matched_cat.type == tx_type:
                    return matched_cat
                    
        # If no match, return default category by transaction type
        fallback_name = "Salary" if tx_type == "income" else "Shopping"
        fallback_cat = next((c for c in categories if c.name == fallback_name), None)
        
        # Absolute fallback if categories are missing from database
        if not fallback_cat:
            fallback_cat = next((c for c in categories if c.type == tx_type), None)
            
        return fallback_cat
