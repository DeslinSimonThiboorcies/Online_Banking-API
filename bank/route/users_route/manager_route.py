from flask import Blueprint, request, jsonify
from bank.services.user_services.manager.manager_login_services import ManagerRegisterServices
from bank.services.user_services.manager.manager_services import MangerService
from bank.utils.manager_decorator import require_system_admin_
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
        "Message" : "Login Successfull",
        "Bearer" : token
    }), 200

#GET
@manager_bp.route("/manager/profiles", methods = ["GET"])
@require_system_admin_()
def profiles():

    managers = MangerService.view_managers()
    if not managers:
        return jsonify({
            "message" : "Manager not found!"
        }), 404

    response = []
    for manager in managers:
        response.append({
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
        "Message" : "Successfull!",
        "Note" : response
    }), 200

#PROFILE 
@manager_bp.route("/manager/profile/<int:id>", methods = ["GET"])
@jwt_required()
def profile(id):

    manager = get_jwt()
    manager_role = manager.get("role")
    manager_id = int(get_jwt_identity())

    if manager_role != "admin" and manager_id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    managers = MangerService.view_manager(id)
    if not managers:
        return jsonify({
            "Message" : "Manager not found!"
        }), 404

    response = {
        "id": managers.id,
        "full_name": managers.full_name,
        "phone_number": managers.phone_number,
        "email": managers.email,
        "date_of_birth": managers.date_of_birth,
        "address": managers.address,
        "state": managers.state,
        "country": managers.country,
        "zip_code": managers.zip_code,
        "role": managers.role,
        "username": managers.username,
        "created_at": managers.created_at,
        "login_at": managers.login_at            
    }

    return jsonify({
        "Note" : "Success",
        "Message" : response
    }), 200

@manager_bp.route("/manager/update/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    target_manager = MangerService.view_manager(id)
    if not target_manager:
        return jsonify({
            "Message" : "Manager not found!"
        }), 404

    claims = get_jwt()
    if claims.get("role") != "admin":
        manager_id = int(get_jwt_identity())
        current_manager = MangerService.view_manager(manager_id)
        if not current_manager:
            return jsonify({
                "Message" : "Manager not found!"
            }), 404
        if current_manager.id != id:
            return jsonify({
                "Message" : "Access Denied!"
            }), 403

    if claims.get("role") != "admin" and manager_id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        })

    try:
        MangerService.update(target_manager, data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Manager update successfull!"
    }), 200

#DELETE
@manager_bp.route("/manager/delete/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete(id):

    target_manager = MangerService.view_manager(id)
    if not target_manager:
        return jsonify({
            "Message" : "Manager not found!"
        }), 404

    claims = get_jwt()
    if claims.get("role") != "admin":
        manager_id = int(get_jwt_identity())
        current_manager = MangerService.view_manager(manager_id)
        if not current_manager:
            return jsonify({
                "Message" : "Manager not found!"
            }), 404
        if current_manager.id != id:
            return jsonify({
                "Message" : "Access Denied!"
            }), 403

    if claims.get("role") != "admin" and manager_id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    try:
        MangerService.delete(target_manager)

    except ValueError as e:
        return jsonify({
            "massage" : str(e)
        }), 400

    return jsonify({
        "Message" : "Manager delete successfull!"
    }), 200