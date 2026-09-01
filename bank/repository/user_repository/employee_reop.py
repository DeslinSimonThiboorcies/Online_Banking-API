from bank.extensions.db import db
from bank.model.users_model.employee import Employee

class EmployeeRepository:

    @staticmethod
    def create_employee(employee):
        db.session.add(employee)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return Employee.query.filter_by(
            username = username
        )

    @staticmethod
    def get_employees():
        return Employee.query.all()

    @staticmethod
    def get_employee_by_id(employee_id):
        db.session.get(
            Employee,
            employee_id
        )
    @staticmethod
    def update_employee():
        db.session.commit()

    @staticmethod
    def delete_employee(employee):
        db.session.delete(employee)
        db.session.commit()