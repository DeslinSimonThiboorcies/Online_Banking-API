from flask import Blueprint, request, jsonify
from bank.services.user_services.employee.employee_register  import EmployeeRegisterServices
from bank.services.user_services.employee.employee_services import EmployeeServices
from bank.utils.employee_decorator import employee_admin_required
from flask_jwt_extended import get_jwt_identity, jwt_required


employee_bp = Blueprint(
    "employee",
    __name__
)

#Register
@employee_bp.route("/employee/register", methods = ["POST"])
def register():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        }), 400

    try:
        EmployeeRegisterServices.register(data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Employee Created successfull!"
    }), 201

#Login
@employee_bp.route("/employee/login", methods = ["POST"])
def login():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        }), 400

    try:
        token = EmployeeRegisterServices.login(data)

    except ValueError as e:
        return jsonify({
            "Message"  : str(e)
        }), 400

    return jsonify({
        "Bearer" : token
    }), 201

#View all profile:
@employee_bp.route("/employee/view_profile", methods = ["GET"])
@employee_admin_required
@jwt_required()
def all_profiles():

    employee = EmployeeServices.view_all_employee()
    if not employee:
       return jsonify({
           "Employee not found!"
       }), 404

    response = []
    for employees in employee:
        response.append({
        "id": employees.id,
        "full_name": employees.full_name,
        "phone_number": employees.phone_number,
        "email": employees.email,
        "date_of_birth": employees.date_of_birth,
        "address": employees.address,
        "state": employees.state,
        "country": employees.country,
        "zip_code": employees.zip_code,
        "role": employees.role,     
        "username": employees.username,
        "created_at": employees.created_at,
        "login_at": employees.login_at                        
        })

    return jsonify({
        "Message" : response
    }), 200

#View employee
@employee_bp.route("/employee/view_my_profile/<int:id>", methods = ["GET"])
@jwt_required()
def my_profile(id):

    employee_id = int(get_jwt_identity())
    employee = EmployeeServices.view_employee(employee_id)
    if not employee:
        return jsonify({
            "Employee not found!"
        }), 404

    if employee.role not in ["admin", "manager"] and employee.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT ADMIN OR MANAGER"
        }), 403

    response = {
        "id": employee.id,
        "full_name": employee.full_name,
        "phone_number": employee.phone_number,
        "email": employee.email,
        "date_of_birth": employee.date_of_birth,
        "address": employee.address,
        "state": employee.state,
        "country": employee.country,
        "zip_code": employee.zip_code,
        "role": employee.role,     
        "username": employee.username,
        "created_at": employee.created_at,
        "login_at": employee.login_at    
    }

    return jsonify({
        "Message" : response
    }), 200

#update
@employee_bp.route("/employee/upate/my_profile/<int:id>", methods = ["PUT"])
@jwt_required()
def update(id):

    employee_id = int(get_jwt_identity())
    employee = EmployeeServices.view_employee(employee_id)
    if not employee:
        return jsonify({
            "Employee not found!"
        }), 404

    if employee.role not in ["admin", "manager"] and employee.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT ADMIN OR MANAGER"
        }), 403

    data = request.get_json(silent=True)

    try:
        EmployeeServices.update(employee, data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Employee Update succcessfull!"
    }), 200

#delete
@employee_bp.route("/employee/delete/my_profile/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete(id):

    employee_id = int(get_jwt_identity())
    employee = EmployeeServices.view_employee(employee_id)
    if not employee:
        return jsonify({
            "Employee not found!"
        }), 404
    
    if employee.role not in ["admin", "manager"] and employee.id != id:
        return jsonify({
            "MESSAGE": "ACCESS DENIED CONTACT ADMIN OR MANAGER"
        }), 403
    
    try:
        EmployeeServices.delete(employee)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400
    
    return jsonify({
        "Message" : "Employee Update succcessfull!"
    }), 200