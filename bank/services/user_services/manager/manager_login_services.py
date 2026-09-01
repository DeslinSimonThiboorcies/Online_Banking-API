from bank.model.users_model.manager import Manager
from bank.repository.user_repository.manager_repo import ManagerRepository
from flask_jwt_extended import create_access_token

class ManagerRegisterServices:

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
        username = data.get("username")
        password = data.get("password")

        existing_manager = ManagerRepository.get_by_username(username)
        if existing_manager:
            raise ValueError(
                "MANAGER ALREADY EXIST"
            )

        managers = Manager(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth = date_of_birth,
            address=address,
            state = state,
            country = country,
            zip_code = zip_code,
            username=username
        )

        managers.manager_password(password)
        managers = ManagerRepository.create_manager(managers)
        return managers

    @staticmethod
    def login(data):

        username = data.get("username")
        password = data.get("password")

        manager = ManagerRepository.get_by_username(username)
        
        if not manager:
            raise ValueError(
                "Manager not found!"
            )

        if not manager.check_manager_password(password):
            raise ValueError(
                "Password or Email Invalid"
            )

        token = create_access_token(
            identity=str(manager.id)
        )

        return token