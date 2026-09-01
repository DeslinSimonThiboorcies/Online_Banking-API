from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from bank.repository.user_repository.manager_repo import ManagerRepository

def manager_admin_required(func):

    @wraps(func)
    def decorator(*args, **kwargs):

        manager_id = int(get_jwt_identity())
        current_manager = ManagerRepository.get_manager_by_id(manager_id)

        if not current_manager or current_manager.role != 'admin':
            return jsonify({
                "message": "Admin access required"
            }), 403

        return func(*args, **kwargs)
    return decorator