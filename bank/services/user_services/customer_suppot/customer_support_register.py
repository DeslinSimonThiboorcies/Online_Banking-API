from bank.model.users_model.customer_support import CustomerSupport
from bank.repository.user_repository.customer_sup_reop import CustomerSupportRepository
from flask_jwt_extended import create_access_token

class CustomerRegisterServices:

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
        language = data.get("language")
        username = data.get("username")
        password = data.get("password")

        existing_customer_service = CustomerSupportRepository.get_by_username(username)
        if existing_customer_service:
            raise ValueError(
                "USER ALREADY EXIST"
        )

        cs = CustomerSupport(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth = date_of_birth,
            address=address,
            state = state,
            country = country,
            zip_code = zip_code,
            language = language,
            username=username
        )

        cs.customer_support_password(password)
        CustomerSupportRepository.create_customer_support(cs)
        return cs
    
    @staticmethod
    def login(data):

        username = data.get("username")
        password = data.get("password")

        customer_service = CustomerSupportRepository.get_by_username(username)
        if not customer_service:
            raise ValueError(
                "customer not found!"
            )

        if not customer_service.check_customer_support_password(password):
            raise ValueError(
                "Password or Email Invalid"
            )

        token = create_access_token(
            identity=str(customer_service.id)
        )
        return token