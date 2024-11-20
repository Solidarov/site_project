from flask_login import current_user
from functools import wraps
from flask import jsonify

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized access", "message": "Login required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def api_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "Unauthorized access", "message": "You're not admin"}), 403
        return f(*args, **kwargs)
    return decorated_function