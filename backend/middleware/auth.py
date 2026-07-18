from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def token_required(f):
    """
    Custom decorator to guard routes and ensure a valid user session.
    Automatically fetches the database User object and passes it to the handler as 'current_user'.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Verify JWT exists in headers or cookies
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Fetch user from database
            current_user = User.query.get(user_id)
            if not current_user:
                return jsonify({
                    "error": "Unauthorized",
                    "message": "User not found in system."
                }), 401
                
        except Exception as e:
            return jsonify({
                "error": "Unauthorized",
                "message": str(e)
            }), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated
