from flask import Blueprint, request, jsonify
from bank.services.user_services.customer.customer_register import Customer_Service
from bank.services.user_services.customer.customer_services import CustomerServices
from bank.utils.customer_decorector import customer_admin_required
from flask_jwt_extended import get_jwt_identity, jwt_required

customer_bp = Blueprint(
    "customer",
    __name__
)

#Register
@customer_bp.route("/customer/register", methods = ["POST"])
def register():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "Message" : "request body must be json"
        }), 400

    try:
        Customer_Service.register(data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "User create successfull!"
    }), 201

#Login
@customer_bp.route("/customer/login", methods = ["POST"])
def login():

    data = request.get_json(silent= True)
    if not data:
        return jsonify({
            "Message" : "request body must be json"
        }), 400

    try:
        token = Customer_Service.login(data)

    except ValueError as e:
        return jsonify({
            "massage" : str(e)
        }), 400

    return jsonify({
        "Bearer" : token
    }), 200

#View all profiles
@customer_bp.route("/customer/profile", methods = ["GET"])
@customer_admin_required
@jwt_required()
def all_profile():

    customer = CustomerServices.view_all_user()
    if not customer:
        return jsonify({
            "Message" : "customer not found!"
        }), 404

    response = []
    for customers in customer_bp:
        response.append({
        "id": customers.id,
        "full_name": customers.full_name,
        "phone_number": customers.phone_number,
        "email": customers.email,
        "date_of_birth": customers.date_of_birth,
        "address": customers.address,
        "state": customers.state,
        "country": customers.country,
        "zip_code": customers.zip_code,        
        "role": customers.role,
        "kyc_status" : customer.kyc_status,
        "username": customers.username,
        "is_activate" : customer.is_activate,
        "created_at": customers.created_at,
        "login_at": customers.login_at           
        })

    return jsonify({
        "Messgae" : response
    }), 200

#view profile
@customer_bp.route("/customer/my_profile/<int:id>", methods = ["GET"])
@jwt_required()
def profile(id):

    customer_id = int(get_jwt_identity())
    customer = CustomerServices.view_user(customer_id)
    if not customer:
        return jsonify({
            "Messge" : "User not found!"
        }), 404

    if customer.role not in ["admin", "manager", "customer_support"] and customer.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT MANAGER OR ADMIN!"
        }), 403

    response = {
        "id": customer.id,
        "full_name": customer.full_name,
        "phone_number": customer.phone_number,
        "email": customer.email,
        "date_of_birth": customer.date_of_birth,
        "address": customer.address,
        "state": customer.state,
        "country": customer.country,
        "zip_code": customer.zip_code,        
        "role": customer.role,
        "kyc_status" : customer.kyc_status,
        "username": customer.username,
        "is_activate" : customer.is_activate,
        "created_at": customer.created_at,
        "login_at": customer.login_at
    }       

    return jsonify({
        "Message" :response
    }), 200

#update users
@customer_bp.route("/customer/update/my_profile/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    customer_id = int(get_jwt_identity())
    customer = CustomerServices.view_user(customer_id)
    if not customer:
        return jsonify({
            "Messge" : "User not found!"            
        }), 404

    if customer.role not in ["admin", "manager", "customer_support"] and customer.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT MANAGER OR ADMIN!"
        }), 403

    data = request.get_json(silent= True)

    try:
        CustomerServices.update(customer, data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "customer update successfull!"
    }), 200

#Delete profiles
@customer_bp.route("/customer/delete/my_profile/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    customer_id = int(get_jwt_identity())
    customer = CustomerServices.view_user(customer_id)
    if not customer:
        return jsonify({
            "Messge" : "User not found!"            
        }), 404

    if customer.role not in ["admin", "manager", "customer_support"] and customer.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT MANAGER OR ADMIN!"
        }), 403

    data = request.get_json(silent= True)

    try:
        CustomerServices.delete(customer)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Customer deleted successfull!"
    }), 200