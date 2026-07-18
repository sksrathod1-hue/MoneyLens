from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Binds global error handlers to the Flask application."""
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        response = jsonify({
            "error": e.name,
            "message": e.description,
            "code": e.code
        })
        response.status_code = e.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """Global fallback error handler for unhandled backend exceptions."""
        app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        
        # Check if debugging mode is active
        message = str(e) if app.config.get("DEBUG") else "An internal server error occurred."
        
        response = jsonify({
            "error": "Internal Server Error",
            "message": message,
            "code": 500
        })
        response.status_code = 500
        return response
