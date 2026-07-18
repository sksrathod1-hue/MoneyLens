import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database.database import db

def create_app(config_class=Config):
    """Application factory for MoneyLens backend Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Extensions
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Create upload directories if they don't exist
    os.makedirs(app.config["RECEIPT_UPLOAD_DIR"], exist_ok=True)
    os.makedirs(app.config["STATEMENT_UPLOAD_DIR"], exist_ok=True)
    
    # Create placeholder files in upload dirs to ensure they are tracked
    with open(os.path.join(app.config["RECEIPT_UPLOAD_DIR"], ".gitkeep"), "a"):
        pass
    with open(os.path.join(app.config["STATEMENT_UPLOAD_DIR"], ".gitkeep"), "a"):
        pass
        
    # Register error handlers
    from middleware.error_handler import register_error_handlers
    register_error_handlers(app)
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.transactions import transactions_bp
    from routes.reports import reports_bp
    from routes.budgets import budgets_bp
    from routes.profile import profile_bp
    from routes.settings import settings_bp
    from routes.sms import sms_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(budgets_bp, url_prefix="/api/budgets")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(settings_bp, url_prefix="/api/settings")
    app.register_blueprint(sms_bp, url_prefix="/api/sms")
    
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "MoneyLens API is fully operational"
        }), 200
        
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config["PORT"], debug=app.config["DEBUG"])
