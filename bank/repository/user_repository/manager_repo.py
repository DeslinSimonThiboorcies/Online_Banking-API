from bank.extensions.db import db
from bank.model.users_model.manager import Manager

class ManagerRepository:

    @staticmethod
    def create_manager(manager):
        db.session.add(manager)
        db.session.commit()

    @staticmethod
    def get_by_username(username):

        return Manager.query.filter_by(
            username = username
        ).first()

    @staticmethod
    def get_manager():
        return Manager.query.all()

    @staticmethod
    def get_manager_by_id(manager_id):
        return db.session.get(
            Manager,
            manager_id
        )

    @staticmethod
    def update_manager():
        db.session.commit()

    @staticmethod
    def delete_manager(manager):
        db.session.delete(manager)
        db.session.commit()