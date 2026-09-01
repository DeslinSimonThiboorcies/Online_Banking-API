from bank.extensions.db import db
from bank.model.users_model.customer_support import CustomerSupport

class CustomerSupportRepository:

    @staticmethod
    def create_customer_support(customer_support):
        db.session.add(customer_support)
        db.session.commit()

    @staticmethod
    def get_customer_services():
        return CustomerSupport.query.all()

    @staticmethod
    def get_by_username(username):
            return CustomerSupport.query.filter_by(
            username = username
        ).first()

    @staticmethod
    def get_customer_support_by_id(customer_support_id):
        db.session.get(
            CustomerSupport,
            customer_support_id
        )

    @staticmethod
    def update_customer_support():
        db.session.commit()

    @staticmethod
    def delete_customer_support(customer_support):
        db.session.delete(customer_support)
        db.session.commit()