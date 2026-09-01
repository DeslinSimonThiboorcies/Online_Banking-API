from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from bank.repository.user_repository.customer_repo import CustomerRepository

def Admin_require_customer(func):

    @wraps(func)
    def decorator(*args, **kwargs):

        customer_id = int(get_jwt_identity())
        customer = CustomerRepository.get_customer_by_id(customer_id)

        if not customer:
            return jsonify({
                "MESSAGE": "Invalid or expired session"
            }), 401


        if customer.role not in ["admin", "manager"]:
            return jsonify({
                "MESSAGE": "ACCESS DENIED CONTACT ADMIN OR MANAGER"
            }), 403

        return func(*args, **kwargs)
    return decorator
