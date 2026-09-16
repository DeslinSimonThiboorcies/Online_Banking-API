from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def require_manager_():
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != "manager":
                return jsonify({"message": "Managers only!"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_system_admin_():
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"message": "Admin access required"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator