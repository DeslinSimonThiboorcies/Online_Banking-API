from flask import Blueprint, request, jsonify
from bank.services.user_services.admin_services.admin_services import AdminServices
from bank.services.user_services.admin_services.admin_login_services import AdminRegisterService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


admin_bp = Blueprint(
    "admin",
    __name__
)

def require_admin_():

    claims = get_jwt()
    return claims.get("role") == "admin"

#REGISTATION
@admin_bp.route("/admin/register", methods=["POST"])
def register():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        }), 400

    try:
        AdminRegisterService.register(data)

    except ValueError as e:
        return jsonify({
            "message" : str(e)
        }), 400

    return jsonify({
        "message": "Admin created successfully!"
    }), 201

#LOGIN
@admin_bp.route("/admin/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
         "message": "Request body must be JSON."
        }), 400

    try:
        token = AdminRegisterService.login(data)

    except ValueError:
        return jsonify({
            "message": "Invalid username or password."
        }), 401

    return jsonify({
        "message": "Login successful!",
        "Bearer" : token
    }), 200

#GET / PROFILE
@admin_bp.route("/admin/profile", methods=["GET"])
@jwt_required()
def profile():

    if not require_admin_():
        return jsonify({
            "message" : "Access denied!"
        }), 403

    admin_id = get_jwt_identity()
    admin = AdminServices.view_admin(admin_id)
    if not admin:
        return jsonify({
            "message": "Admin not found!"
        }), 404

    return jsonify({
        "id": admin.id,
        "full_name": admin.full_name,
        "phone_number": admin.phone_number,
        "email": admin.email,
        "date_of_birth": admin.date_of_birth,
        "username": admin.username,
        "role": admin.role,
        "address": admin.address,
        "state": admin.state,
        "country": admin.country,
        "zip_code": admin.zip_code,
        "created_at": admin.created_at,
        "login_at": admin.login_at,
    }), 200

#UPDATE
@admin_bp.route("/admin/update/<int:admin_id>", methods=["PUT"])
@jwt_required()
def update_profile(admin_id):

    if not require_admin_():
        return jsonify({
            "message" : "Access denied!"
        }), 403

    admin = AdminServices.view_admin(admin_id)
    if not admin:
        return jsonify({
            "message": "Admin not found!"
        }), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        })

    try:
        AdminServices.update(admin, data)

    except ValueError as e:
        return jsonify({
            "message" : str(e)
        }), 400

    return jsonify({
        "message": "Admin updated successfully!"
    }), 200

#DELETE
@admin_bp.route("/admin/delete/<int:admin_id>", methods=["DELETE"])
@jwt_required()
def remove_admin(admin_id):

    admin = AdminServices.view_admin(admin_id)
    if not admin:
        return jsonify({
            "message": "Request body must be JSON."
        }), 404

    AdminServices.delete(admin)
    return jsonify({
        "message": "Admin deleted successfully!"
    })