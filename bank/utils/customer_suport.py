from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from bank.repository.user_repository.customer_sup_reop import CustomerSupportRepository

def admin_required(func):

    @wraps(func)
    def decorator(*args, **kwargs):

        customer_suport_id = int(get_jwt_identity())
        customer_suport = CustomerSupportRepository.get_customer_support_by_id(customer_suport_id)

        if not customer_suport or customer_suport.role not in ["admin", "manager"]:
            return jsonify({
                "message": "Admin or Manager access required"
            }), 403

        return func(*args, **kwargs)
    return decorator
