from bank.model.users_model.employee import Employee
from bank.repository.user_repository.employee_reop import EmployeeRepository
from flask_jwt_extended import create_access_token

class EmployeeRegisterServices:

    @staticmethod
    def register(data):

        full_name = data.get("full_name")
        phone_number = data.get("phone_number")
        email = data.get("email")
        date_of_birth = data.get("date_of_birth")
        address = data.get("address")
        state = data.get("state")
        country = data.get("country")
        zip_code = data.get("zip_code")
        role = data.get("role")
        username = data.get("username")
        password = data.get("password")

        existing_emplyee = EmployeeRepository.get_by_username(username)
        if existing_emplyee:
            raise ValueError(
                "EMPLOYEE ALREADY EXIST"
        )

        employee = Employee(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth = date_of_birth,
            address=address,
            state = state,
            country = country,
            zip_code = zip_code,
            role = role,
            username=username
        )

        employee.employee_password(password)
        EmployeeRepository.create_employee(employee)
        return employee
    
    @staticmethod
    def login(data):

        username = data.get("username")
        password = data.get("password")

        employee = EmployeeRepository.get_by_username(username)
        if not employee:
            raise ValueError(
                "employee not found!"
            )

        if not employee.check_employee_password(password):
            raise ValueError(
                "Password or Email Invalid"
            )

        token = create_access_token(
            identity=str(employee.id)
        )
        return token