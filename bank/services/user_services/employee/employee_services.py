from bank.repository.user_repository.employee_reop import EmployeeRepository

class EmployeeServices:

    @staticmethod
    def view_all_employee():

        return EmployeeRepository.get_employees()

    @staticmethod
    def view_employee(employee_id):
        return EmployeeRepository.get_employee_by_id(employee_id)
    
    @staticmethod
    def update(employee, data):

       employee.full_name = data.get("full_name", employee.full_name)
       employee.phone_number = data.get("phone_number", employee.phone_number)
       employee.email = data.get("email", employee.email)
       employee.address = data.get("address", employee.address)
       employee.date_of_birth = data.get("date_of_birth", employee.date_of_birth)
       employee.state = data.get("state", employee.state)
       employee.country = data.get("country", employee.country)
       employee.zip_code = data.get("zip_code", employee.zip_code)
       employee.role = data.get("role", employee.role)
       employee.username = data.get("username", employee.username)

       EmployeeRepository.update_employee()
       return employee

    @staticmethod
    def delete(employee):

        EmployeeRepository.delete_employee(employee)
        return True