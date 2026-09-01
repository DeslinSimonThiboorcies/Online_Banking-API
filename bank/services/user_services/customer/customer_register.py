from bank.model.users_model.customer import Customer
from bank.repository.user_repository.customer_repo import CustomerRepository
from flask_jwt_extended import create_access_token

class Customer_Service:

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

        existing_customer = CustomerRepository.get_by_username(username)
        if existing_customer:
            raise ValueError(
                "USER ALREADY EXIST"
        )

        customers = Customer(
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

        customers.customer_password(password)
        CustomerRepository.create_customer(customers)
        return customers
    
    @staticmethod
    def login(data):

        username = data.get("username")
        password = data.get("password")

        customer = CustomerRepository.get_by_username(username)
        if not customer:
            raise ValueError(
                "customer not found!"
            )

        if not customer.check_customer_password(password):
            raise ValueError(
                "Password or Email Invalid"
            )

        token = create_access_token(
            identity=str(customer.id)
        )
        return token