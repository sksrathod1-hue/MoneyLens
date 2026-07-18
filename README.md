# MoneyLens

MoneyLens is a smart personal finance management web application designed to help users track expenses, manage budgets, analyze income/spending trends, and receive AI-driven financial insights. It also supports parsing incoming transaction SMS messages to automatically log expenses.

## Project Structure

```
MoneyLens/
├── backend/            # Python Flask backend
│   ├── database/       # SQLite database, schema, and seeding
│   ├── models/         # SQLAlchemy models (User, Transaction, etc.)
│   ├── routes/         # Flask blueprints (Auth, Transactions, etc.)
│   ├── services/       # Core business logic (SMS Parsing, AI insights)
│   ├── middleware/     # Auth and error handling filters
│   ├── utils/          # Helpers, security, constants, and logging
│   └── tests/          # pytest unit/integration tests
├── frontend/           # HTML/CSS/JS single-page-like dynamic application
│   ├── assets/         # CSS styles, JS handlers, and assets
│   └── components/     # Reusable HTML sub-layouts
└── docs/               # Technical documents and manuals
```

## Getting Started

### Prerequisites
- Python 3.8+
- Modern Web Browser

### Installation & Setup

1. **Clone/Navigate to project**:
   ```bash
   cd MoneyLens/backend
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**:
   ```bash
   python -c "from database.database import init_db; init_db()"
   python database/seed.py
   ```

5. **Start Flask Server**:
   ```bash
   python app.py
   ```

6. **Run Frontend**:
   Open `frontend/index.html` in your web browser.

## License
MIT License.
