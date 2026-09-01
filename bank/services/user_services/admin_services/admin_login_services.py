from bank.model.users_model.admin import Admin
from bank.repository.user_repository.admin_repo import AdminRepository
from flask_jwt_extended import create_access_token

class AdminRegisterService:

    @staticmethod
    def register(data):

        full_name = data.get("full_name")
        phone_number = data.get("phone_number")
        email = data.get("email")
        date_of_birth = data.get("date_of_birth")
        username = data.get("username")
        address = data.get("address")
        state = data.get("state")
        country = data.get("country")
        zip_code = data.get("zip_code")
        password = data.get("password")

        existing_admin = AdminRepository.get_by_username(username)

        if existing_admin:
            raise ValueError(
                "ADMIN ALREADY EXIST"
            )

        admin = Admin(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth = date_of_birth,
            username=username,
            address=address,
            state = state,
            country = country,
            zip_code = zip_code
        )
        admin.admin_password(password)
        AdminRepository.create_admin(admin)
        return admin

    @staticmethod
    def login(data):

        username = data.get("username")
        password = data.get("password")

        admin = AdminRepository.get_by_username(username)

        if not admin:
            raise ValueError(
                "admin not found!"
            )

        if not admin.check_admin_password(password):
            raise ValueError(
                "Password or Email Invalid"
            )

        token = create_access_token(
            identity=str(admin.id),
            additional_claims={"role" : admin.role}
        )

        return token