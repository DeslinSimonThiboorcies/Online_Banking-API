from flask import Blueprint, request, jsonify
from bank.services.user_services.manager.manager_login_services import ManagerRegisterServices
from bank.services.user_services.manager.manager_services import MangerService
from bank.utils.manager_decorator import manager_admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

manager_bp = Blueprint(
    "manager",
    __name__
)

#REGISTER
@manager_bp.route("/manager/register", methods = ["POST"])
def register():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        }), 400

    try:
        ManagerRegisterServices.register(data)

    except ValueError as e:
        return jsonify({
            "message": str(e)            
        }), 400

    return jsonify({
        "message": "Manager created successfully!"        
    }), 201

#LOIGN
@manager_bp.route("/manager/login", methods = ["POST"])
def login():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        }), 400

    try:
        token = ManagerRegisterServices.login(data)

    except ValueError:
        return jsonify({
            "message": "Invalid username or password."
        }), 401

    return jsonify({
        "Bearer" : token
    }), 200

#GET
@manager_bp.route("/manager/profiles", methods = ["GET"])
@manager_admin_required
@jwt_required()
def profiles():

    managers = MangerService.view_managers()
    if not managers:
        return jsonify({
            "message" : "Manager not found!"
        }), 404

    respons = []

    for manager in managers:
        respons.append({
        "id": manager.id,
        "full_name": manager.full_name,
        "phone_number": manager.phone_number,
        "email": manager.email,
        "date_of_birth": manager.date_of_birth,
        "address": manager.address,
        "state": manager.state,
        "country": manager.country,
        "zip_code": manager.zip_code,
        "role": manager.role,
        "username": manager.username,
        "created_at": manager.created_at,
        "login_at": manager.login_at            
        })

    return jsonify({
        "message" : respons
    }), 201

#PROFILE 
@manager_bp.route("/manager/profile/<int:id>", methods = ["GET"])
@jwt_required()
def profile(id):

    manager_id = int(get_jwt_identity())
    manager = MangerService.view_manager(manager_id)
    if not manager:
        return jsonify({
            "Message" : "Manager not found!"
        }), 404

    if manager.role != "admin" and manager.id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    response = {
        "id": manager.id,
        "full_name": manager.full_name,
        "phone_number": manager.phone_number,
        "email": manager.email,
        "date_of_birth": manager.date_of_birth,
        "address": manager.address,
        "state": manager.state,
        "country": manager.country,
        "zip_code": manager.zip_code,
        "role": manager.role,
        "username": manager.username,
        "created_at": manager.created_at,
        "login_at": manager.login_at            
    }

    return jsonify({
        "Message" : response
    }), 201

@manager_bp.route("/manager/update/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    manager_id = int(get_jwt_identity())
    manager = MangerService.view_manager(manager_id)
    if not manager:
        return jsonify({
            "Message" : "Manager not found!"
        }), 404
    
    if manager.role != "admin" and manager.id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        })

    try:
        MangerService.update(manager, data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Manager update successfull!"
    }), 201

#DELETE
@manager_bp.route("/manager/delete/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete(id):

    manager_id = int(get_jwt_identity())
    manager = MangerService.view_manager(manager_id)
    if not manager:
        return jsonify({
            "Message" : "Manager not found!"
        }), 404

    if manager.role != "admin" and manager.id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    try:
        MangerService.delete(manager)

    except ValueError as e:
        return jsonify({
            "massage" : str(e)
        }), 400

    return jsonify({
        "Message" : "Manager delete successfull!"
    }), 201