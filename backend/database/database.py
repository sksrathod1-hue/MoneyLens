import os
from flask_sqlalchemy import SQLAlchemy

# Declare db extension instance
db = SQLAlchemy()

def init_db():
    """Helper function to initialize SQLite database with raw schema.sql if needed."""
    from app import create_app
    app = create_app()
    with app.app_context():
        # Get path of database file
        # Check database engine, if SQLite, we can initialize it from schema.sql
        db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        if db_uri.startswith("sqlite:///"):
            # Check schema file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            schema_path = os.path.join(base_dir, "database", "schema.sql")
            
            # Read schema.sql
            if os.path.exists(schema_path):
                print(f"Initializing database from {schema_path}...")
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema_sql = f.read()
                
                # Execute the raw SQL commands
                conn = db.engine.raw_connection()
                try:
                    cursor = conn.cursor()
                    cursor.executescript(schema_sql)
                    conn.commit()
                    print("Database schema loaded successfully.")
                except Exception as e:
                    print(f"Error executing schema script: {e}")
                    conn.rollback()
                finally:
                    conn.close()
            else:
                print(f"Schema file not found at {schema_path}, creating standard SQLAlchemy tables.")
                db.create_all()
        else:
            db.create_all()
            print("Non-SQLite database detected, standard tables created.")
