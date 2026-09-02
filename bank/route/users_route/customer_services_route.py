from flask import Blueprint, request, jsonify
from bank.services.user_services.customer_suppot.customer_support_register import CustomerRegisterServices
from bank.services.user_services.customer_suppot.customer_support_service import CustomerSupportServices
from bank.utils.customer_suport import admin_required
from flask_jwt_extended import get_jwt_identity, jwt_required

c_s_bp = Blueprint(
    "customer_support",
    __name__
)

#Register
@c_s_bp.route("/user/register", methods = ["POST"])
def register():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "Message" : "request body must be json"
        }), 400

    try:
        CustomerRegisterServices.register(data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "User create successfull!"
    }), 201

#Login
@c_s_bp.route("/user/login", methods = ["POST"])
def login():

    data = request.get_json(silent= True)
    if not data:
        return jsonify({
            "Message" : "request body must be json"
        }), 400

    try:
        token = CustomerRegisterServices.login(data)

    except ValueError as e:
        return jsonify({
            "massage" : str(e)
        }), 400

    return jsonify({
        "Bearer" : token
    }), 200

#View all profiles
@c_s_bp.route("/user/profile", methods = ["GET"])
@admin_required
@jwt_required()
def all_profile():

    user = CustomerSupportServices.view_all_user()
    if not user:
        return jsonify({
            "Message" : "User not found!"
        }), 404

    response = []
    for users in user:
        response.append({
        "id": users.id,
        "full_name": users.full_name,
        "phone_number": users.phone_number,
        "email": users.email,
        "date_of_birth": users.date_of_birth,
        "address": users.address,
        "state": users.state,
        "country": users.country,
        "zip_code": users.zip_code,        
        "role": users.role,
        "language" : users.language,
        "username": users.username,
        "created_at": users.created_at,
        "login_at": users.login_at,              
        })

    return jsonify({
        "Messgae" : response
    }), 200

#view profile
@c_s_bp.route("/user/my_profile/<int:id>", methods = ["GET"])
@jwt_required()
def profile(id):

    customer_helper_id = int(get_jwt_identity())
    customer_suport = CustomerSupportServices.view_user(customer_helper_id)
    if not customer_suport:
        return jsonify({
            "Messge" : "User not found!"
        }), 404

    if customer_suport.role not in ["admin", "manager"] and customer_suport.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT MANAGER OR ADMIN!"
        }), 403

    response = {
        "id": customer_suport.id,
        "full_name": customer_suport.full_name,
        "phone_number": customer_suport.phone_number,
        "email": customer_suport.email,
        "date_of_birth": customer_suport.date_of_birth,
        "address": customer_suport.address,
        "state": customer_suport.state,
        "country": customer_suport.country,
        "zip_code": customer_suport.zip_code,        
        "role": customer_suport.role,
        "language" : customer_suport.language,
        "username": customer_suport.username,
        "created_at": customer_suport.created_at,
        "login_at": customer_suport.login_at,                  
    }

    return jsonify({
        "Message" :response
    }), 200

#update users
@c_s_bp.route("/user/update/my_profile/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    customer_helper_id = int(get_jwt_identity())
    customer_suport = CustomerSupportServices.view_user(customer_helper_id)
    if not customer_suport:
        return jsonify({
            "Messge" : "User not found!"            
        }), 404

    if customer_suport.role not in ["admin", "manager"] and customer_suport.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT MANAGER OR ADMIN!"
        }), 403

    data = request.get_json(silent= True)

    try:
        CustomerSupportServices.update(customer_suport , data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "User update successfull!"
    }), 200

#Delete profiles
@c_s_bp.route("/user/delete/my_profile/<int:id>", methods = ["PUT"])
@jwt_required()
def delete_profile(id):

    customer_helper_id = int(get_jwt_identity())
    customer_suport = CustomerSupportServices.view_user(customer_helper_id)
    if not customer_suport:
        return jsonify({
            "Messge" : "User not found!"            
        }), 404
    
    if customer_suport.role not in ["admin", "manager"] and customer_suport.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT MANAGER OR ADMIN!"
        }), 403

    try:
        CustomerSupportServices.delete(customer_suport)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "User delete successfull1"
    }), 200