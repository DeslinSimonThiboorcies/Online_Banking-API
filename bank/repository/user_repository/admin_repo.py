from bank.extensions.db import db
from bank.model.users_model.admin import Admin

class AdminRepository:

    @staticmethod
    def create_admin(admin):
        db.session.add(admin)
        db.session.commit()

    @staticmethod
    def get_by_username(username):

        return Admin.query.filter_by(
            username = username
        ).first()

    @staticmethod
    def get_admin_by_id(admin_id):

        return db.session.get(
            Admin,
            admin_id
        )

    @staticmethod
    def update_admin():
        db.session.commit()

    @staticmethod
    def delete_admin(admin):
        db.session.delete(admin)
        db.session.commit()


# from bank.services.validators.staff_contact_validator import StaffContactValidator

# class AdminRegisterService:
#     @staticmethod
#     def register(data):
#         StaffContactValidator.assert_phone_and_email_available(
#             phone_number=data['phone_number'],
#             email=data['email'],
#         )
#         # ... proceed to create the Admin row