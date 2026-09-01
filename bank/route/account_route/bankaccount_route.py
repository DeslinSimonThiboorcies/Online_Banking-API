from flask import Blueprint, request, jsonify
from bank.services.account_services.bank_account_services import AccountServices
from bank.services.user_services.customer.customer_services import CustomerServices
from flask_jwt_extended import jwt_required, get_jwt_identity
from bank.utils.customer_decorector import customer_admin_required
from bank.utils.bank_account_deco import Admin_require_customer

account_bp = Blueprint(
    "BankAccount",
    __name__
)

#Account Creation
@account_bp.route("/bank/account/creation", methods = ["POST"])
@jwt_required()
def account():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "message": "Request body must be JSON."
        }), 400

    try:
        AccountServices.create_account(data)

    except ValueError as e:
        return jsonify({
            "Message" : "Account create successfull!"
        }), 201

#View Account
@account_bp.route("/bank/account/profile", methods = ["GET"])
@customer_admin_required
@jwt_required()
def view_all_account():

    bank_account = AccountServices.users_accounts()
    if not bank_account:
        return jsonify({
            "message": "User Account Not Found!"
        }), 404

    response = []
    for account in bank_account:
        response.append({
            "id": account.id,
            "user_id": account.user_id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": float(account.balance),
            "branch_name": account.branch_name,
            "status": account.status,
            "created_at": account.created_at.isoformat() if account.created_at else None,
            "snapshot_full_name": account.snapshot_full_name,
            "snapshot_username": account.snapshot_username,
            "snapshot_phone_number": account.snapshot_phone_number,
            "snapshot_email": account.snapshot_email,
            "snapshot_address": account.snapshot_address,
            "snapshot_state": account.snapshot_state,
            "snapshot_taken_at": account.snapshot_taken_at.isoformat() if account.snapshot_taken_at else None,
        })

    return jsonify({
        "Message" : response
    }), 200

@account_bp.route("/bank/account/my_profile/<int:id>", methods = ["GET"])
@jwt_required()
def view_account(id):

    current_user_id = int(get_jwt_identity())
    current_user = CustomerServices.view_user(current_user_id)
    if not current_user:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    if current_user.role not in ["admin", "manager", "customer_support"] and current_user.id != id:
        return jsonify({
            "Message" : "Access Denied!"
        }), 403

    bank = AccountServices.user_account(id)
    if not bank:
        return jsonify({
            "message": "User Account Not Found!"
        }), 404

    response = {
            "id": account.id,
            "user_id": account.user_id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "balance": float(account.balance),
            "branch_name": account.branch_name,
            "status": account.status,
            "created_at": account.created_at.isoformat() if account.created_at else None,
            "snapshot_full_name": account.snapshot_full_name,
            "snapshot_username": account.snapshot_username,
            "snapshot_phone_number": account.snapshot_phone_number,
            "snapshot_email": account.snapshot_email,
            "snapshot_address": account.snapshot_address,
            "snapshot_state": account.snapshot_state,
            "snapshot_taken_at": account.snapshot_taken_at.isoformat() if account.snapshot_taken_at else None,

    }

    return jsonify({
        "Message" : response
    }), 200

#Update bank account
@account_bp.route("/update/bank/account/<int:id>", methods = ["PUT"])
@customer_admin_required
@jwt_required()
def update_account(id):

    bank_account = AccountServices.user_account(id)
    if not bank_account:
        return jsonify({
            "message": "User Account Not Found!"
        }), 404

    data = request.get_json(silent=True)

    try:
        AccountServices.update_account(bank_account, data)

    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Account Updated Successfull!"
    }), 200

#Delete Account
@account_bp.route("/delete/bank/account/<int:id>", methods = ["PUT"])
@Admin_require_customer
@jwt_required()
def remove_account(id):

    bank_account = AccountServices.user_account(id)
    if not bank_account:
        return jsonify({
            "message": "User Account Not Found!"
        }), 404
    
    try:
        AccountServices.remove_account(bank_account)
    
    except ValueError as e:
        return jsonify({
            "Message" : str(e)
        }), 400

    return jsonify({
        "Message" : "Account Delete Successfull!"
    }), 200