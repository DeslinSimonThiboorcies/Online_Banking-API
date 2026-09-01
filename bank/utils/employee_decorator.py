from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from bank.repository.user_repository.employee_reop import EmployeeRepository

def employee_admin_required(func):

    @wraps(func)
    def decorator(*args, **kwargs):

        emloyee_id = int(get_jwt_identity())
        employee = EmployeeRepository.get_employee_by_id(emloyee_id)

        if not employee:
            return jsonify({
                "MESSAGE": "Invalid or expired session"
            }), 401


        if employee.role not in ["admin", "manager"]:
            return jsonify({
                "MESSAGE": "ACCESS DENIED CONTACT ADMIN OR MANAGER"
            }), 403

        return func(*args, **kwargs)
    return decorator
