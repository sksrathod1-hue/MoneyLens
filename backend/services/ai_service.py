from models.ai_insight import AIInsight
from models.transaction import Transaction
from models.budget import Budget
from database.database import db
import requests
import json
from config import Config

class AIService:
    """Service to generate financial insights and savings recommendations using AI or Rule-Based fallback."""
    
    @staticmethod
    def get_user_insights(user_id: int):
        """Fetch saved insights from the DB. If none exist, trigger generation."""
        insights = AIInsight.query.filter_by(user_id=user_id).order_by(AIInsight.created_at.desc()).all()
        if not insights:
            # Generate initial insights asynchronously or inline
            AIService.generate_insights(user_id)
            insights = AIInsight.query.filter_by(user_id=user_id).order_by(AIInsight.created_at.desc()).all()
        return insights
        
    @staticmethod
    def generate_insights(user_id: int):
        """Analyze transaction history and create savings recommendations."""
        # 1. Gather User Financial Profile
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        budgets = Budget.query.filter_by(user_id=user_id).all()
        
        if not transactions:
            # Seed default insights
            AIService._save_insight(
                user_id,
                "Welcome to MoneyLens!",
                "Start logging transactions or send expense SMS details to populate insights. We'll analyze your patterns and show savings opportunities here.",
                "saving"
            )
            return
            
        # Calculate summary metrics
        total_income = sum(float(t.amount) for t in transactions if t.type == "income")
        total_expense = sum(float(t.amount) for t in transactions if t.type == "expense")
        savings_rate = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0
        
        # 2. Rule-based recommendations (Fallback or main engine)
        generated_any = False
        
        # Threat: Low savings rate
        if savings_rate < 10 and total_income > 0:
            AIService._save_insight(
                user_id,
                "Optimize Your Savings Rate",
                f"Your current savings rate is {savings_rate:.1f}%. Financial experts recommend saving at least 20% of your income. Consider reviewing your variable categories like 'Groceries' or 'Food & Dining' to cut back.",
                "saving"
            )
            generated_any = True
            
        # Budget warning checks
        for budget in budgets:
            pct = (float(budget.spent) / float(budget.amount)) * 100 if budget.amount > 0 else 0
            if pct > 90:
                AIService._save_insight(
                    user_id,
                    f"Budget Warning: {budget.category.name if budget.category else 'Budget'}",
                    f"You have consumed {pct:.1f}% of your category budget. Try shifting plans for dining or shopping to next month to avoid overdrafts.",
                    "spending"
                )
                generated_any = True
                
        # Category spending spikes
        category_sums = {}
        for t in transactions:
            if t.type == "expense":
                cat_name = t.category.name if t.category else "Uncategorized"
                category_sums[cat_name] = category_sums.get(cat_name, 0.0) + float(t.amount)
                
        if category_sums:
            highest_cat = max(category_sums, key=category_sums.get)
            highest_amt = category_sums[highest_cat]
            if total_expense > 0 and (highest_amt / total_expense) > 0.4:
                AIService._save_insight(
                    user_id,
                    f"Concentrated Spending in {highest_cat}",
                    f"Category '{highest_cat}' represents {((highest_amt/total_expense)*100):.1f}% of your total expenses. Spreading expenses across different fields is a safer financial plan.",
                    "spending"
                )
                generated_any = True
                
        if not generated_any:
            # General financial health insight
            AIService._save_insight(
                user_id,
                "Financial Health Check: Excellent",
                f"You are maintaining a strong budget. Your current savings rate is {savings_rate:.1f}%. Consider setting up automated transfers to an investment index fund to make your savings work for you.",
                "investment"
            )
            
        # 3. Optional LLM (Gemini) API Call if API Key configured
        if Config.AI_API_KEY:
            try:
                # Call Gemini API to generate deep insight
                # Setting a short timeout to prevent blocking application
                headers = {"Content-Type": "application/json"}
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.AI_MODEL_NAME}:generateContent?key={Config.AI_API_KEY}"
                
                # Mock context summary
                context = {
                    "total_income": total_income,
                    "total_expense": total_expense,
                    "savings_rate": savings_rate,
                    "category_spending": category_sums
                }
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Analyze these financial metrics and provide exactly one short, actionable financial advice paragraph with a short title. Format the response as JSON: {{\"title\": \"...\", \"insight\": \"...\", \"category\": \"spending|saving|investment\"}}. Data: {json.dumps(context)}"
                        }]
                    }]
                }
                
                response = requests.post(url, headers=headers, json=payload, timeout=5)
                if response.status_code == 200:
                    resp_json = response.json()
                    raw_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                    # Clean potential markdown wrappers
                    raw_text = raw_text.strip().replace("```json", "").replace("```", "")
                    parsed = json.loads(raw_text)
                    
                    AIService._save_insight(
                        user_id,
                        parsed.get("title", "AI Wealth Suggestion"),
                        parsed.get("insight", "Try to save 10% more this month."),
                        parsed.get("category", "saving")
                    )
            except Exception as e:
                # Silently skip and rely on the rules if AI fails
                print(f"Skipping LLM insight generation: {e}")
                
    @staticmethod
    def _save_insight(user_id: int, title: str, insight: str, category: str):
        """Helper to create and save the insight in database."""
        # Simple duplicate check
        exists = AIInsight.query.filter_by(user_id=user_id, title=title).first()
        if exists:
            return
            
        new_insight = AIInsight(
            user_id=user_id,
            title=title,
            insight=insight,
            category=category
        )
        db.session.add(new_insight)
        db.session.commit()
