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