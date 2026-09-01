from bank.extensions.db import db
from bank.model.users_model.customer import Customer

class CustomerRepository:

    @staticmethod
    def create_customer(customer):
        db.session.add(customer)
        db.session.commit()

    @staticmethod
    def get_by_username(username):

        return Customer.query.filter_by(
            username = username
        )

    @staticmethod
    def get_customers():
        return Customer.query.all()

    @staticmethod
    def get_customer_by_id(customer_id):

        db.session.get(
            Customer,
            customer_id
        )

    @staticmethod
    def update_customer():
        db.session.commit()

    @staticmethod
    def delete_customer(customer):
        db.session.delete(customer)
        db.session.commit()