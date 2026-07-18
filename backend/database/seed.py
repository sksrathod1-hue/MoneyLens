import datetime
import bcrypt
from database.database import db, init_db
from app import create_app

def seed_data():
    """Seed the SQLite database with default categories and a test user."""
    app = create_app()
    with app.app_context():
        # Clean current tables to avoid key conflicts in seeding
        print("Checking if test user exists...")
        from models.user import User
        from models.category import Category
        from models.transaction import Transaction
        from models.budget import Budget
        
        test_user = User.query.filter_by(username="demo").first()
        if test_user:
            print("Test user 'demo' already exists. Skipping seed.")
            return

        print("Seeding initial database data...")
        # 1. Create a demo user
        # Password will be 'demo123'
        hashed_password = bcrypt.hashpw("demo123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        demo_user = User(
            username="demo",
            email="demo@moneylens.com",
            password_hash=hashed_password
        )
        db.session.add(demo_user)
        db.session.commit()
        print(f"Created demo user: {demo_user.username}")

        # 2. Seed Default Categories (user_id = None for system-wide defaults, or associated to demo_user)
        default_categories = [
            # Income Categories
            {"name": "Salary", "type": "income", "icon": "briefcase", "color": "#2ecc71"},
            {"name": "Freelance", "type": "income", "icon": "laptop", "color": "#1abc9c"},
            {"name": "Investments", "type": "income", "icon": "trending-up", "color": "#9b59b6"},
            
            # Expense Categories
            {"name": "Food & Dining", "type": "expense", "icon": "coffee", "color": "#e67e22"},
            {"name": "Rent & Housing", "type": "expense", "icon": "home", "color": "#3498db"},
            {"name": "Utilities", "type": "expense", "icon": "bolt", "color": "#f1c40f"},
            {"name": "Transportation", "type": "expense", "icon": "car", "color": "#34495e"},
            {"name": "Entertainment", "type": "expense", "icon": "film", "color": "#e74c3c"},
            {"name": "Groceries", "type": "expense", "icon": "shopping-cart", "color": "#27ae60"},
            {"name": "Shopping", "type": "expense", "icon": "shopping-bag", "color": "#d35400"},
            {"name": "Medical", "type": "expense", "icon": "heartbeat", "color": "#c0392b"}
        ]
        
        category_objects = []
        for cat in default_categories:
            db_cat = Category(
                user_id=demo_user.id,
                name=cat["name"],
                type=cat["type"],
                icon=cat["icon"],
                color=cat["color"],
                is_default=True
            )
            db.session.add(db_cat)
            category_objects.append(db_cat)
            
        db.session.commit()
        print(f"Seeded {len(default_categories)} categories.")

        # Dictionary mapping category name to their seeded ID
        cat_map = {c.name: c.id for c in category_objects}

        # 3. Seed Sample Transactions for the past two months
        today = datetime.date.today()
        sample_transactions = [
            # Last month
            {"amount": 5000.00, "type": "income", "cat": "Salary", "desc": "Monthly Salary", "days_offset": -30},
            {"amount": 350.00, "type": "income", "cat": "Freelance", "desc": "Website Project", "days_offset": -25},
            {"amount": 1200.00, "type": "expense", "cat": "Rent & Housing", "desc": "Rent payment", "days_offset": -28},
            {"amount": 80.00, "type": "expense", "cat": "Utilities", "desc": "Electric bill", "days_offset": -24},
            {"amount": 45.00, "type": "expense", "cat": "Transportation", "desc": "Gas", "days_offset": -22},
            {"amount": 120.00, "type": "expense", "cat": "Groceries", "desc": "Weekly grocery shopping", "days_offset": -20},
            {"amount": 65.00, "type": "expense", "cat": "Food & Dining", "desc": "Dinner with friends", "days_offset": -18},
            {"amount": 15.00, "type": "expense", "cat": "Entertainment", "desc": "Netflix Subscription", "days_offset": -15},
            
            # This month
            {"amount": 5000.00, "type": "income", "cat": "Salary", "desc": "Monthly Salary", "days_offset": -2},
            {"amount": 1200.00, "type": "expense", "cat": "Rent & Housing", "desc": "Rent payment", "days_offset": -1},
            {"amount": 95.00, "type": "expense", "cat": "Utilities", "desc": "Internet + Electric", "days_offset": 0},
            {"amount": 150.00, "type": "expense", "cat": "Groceries", "desc": "Whole Foods", "days_offset": -3},
            {"amount": 40.00, "type": "expense", "cat": "Food & Dining", "desc": "Lunch", "days_offset": -4},
            {"amount": 120.00, "type": "expense", "cat": "Shopping", "desc": "New Running Shoes", "days_offset": -5}
        ]

        for tx in sample_transactions:
            date_val = today + datetime.timedelta(days=tx["days_offset"])
            new_tx = Transaction(
                user_id=demo_user.id,
                category_id=cat_map[tx["cat"]],
                amount=tx["amount"],
                type=tx["type"],
                description=tx["desc"],
                date=date_val
            )
            db.session.add(new_tx)

        # 4. Seed Budgets for demo user
        # Rent budget
        rent_budget = Budget(
            user_id=demo_user.id,
            category_id=cat_map["Rent & Housing"],
            amount=1500.00,
            spent=1200.00,
            period="monthly",
            start_date=today.replace(day=1),
            end_date=(today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        )
        # Food budget
        food_budget = Budget(
            user_id=demo_user.id,
            category_id=cat_map["Food & Dining"],
            amount=400.00,
            spent=40.00,
            period="monthly",
            start_date=today.replace(day=1),
            end_date=(today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
        )
        db.session.add(rent_budget)
        db.session.add(food_budget)

        db.session.commit()
        print("Database seeded successfully with test records!")

if __name__ == "__main__":
    init_db()
    seed_data()
