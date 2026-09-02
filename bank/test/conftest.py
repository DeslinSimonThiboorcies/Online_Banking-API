import pytest

from bank import creat_app
from bank.config import TestClass
from bank.extensions.db import db as _db
from bank.model.users_model.admin import Admin
from bank.model.users_model.manager import Manager
from bank.model.users_model.customer_support import CustomerSupport
from bank.model.users_model.employee import Employee
from bank.model.users_model.customer import Customer

from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = creat_app()
    app.config.from_object(TestClass)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def create_admin(db):
    def register_admin(
            
    full_name = "test admin",
    phone_number = int(1234567890),
    email = "test@gmail.com",
    date_of_birth = "1990-01-01",
    username = "test_admin00192",
    role = "admin",
    address = "near park golden st.1/23",
    state = "new york",
    country = "usa",
    zip_code = int(10001),
    password = "test_password"
    ):
        admin = Admin(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            username=username,
            role=role,
            address=address,
            state=state,
            country=country,
            zip_code=zip_code
        )
        admin.admin_password(password)
        db.session.add(admin)
        db.session.commit()
        return admin
    return register_admin

@pytest.fixture
def create_manager(db):
    def register_manager(
            
    full_name = "test manager",
    phone_number = int("1234567890"),
    email = "test_manager@gmail.com",
    date_of_birth = "1990-01-01",
    username = "test_manager00192",
    role = "manager",
    address = "near park golden st.1/23",
    state = "new york",
    country = "usa",
    zip_code = int(10001),
    password = "test_password"
    ):
        manager = Manager(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            username=username,
            role=role,
            address=address,
            state=state,
            country=country,
            zip_code=zip_code
        )
        manager.manager_password(password)
        db.session.add(manager)
        db.session.commit()
        return manager
    return register_manager

@pytest.fixture
def create_customer_support(db):
    def register_customer_support(
            
    full_name = "test customer support",
    phone_number = int(1234567890),
    email = "test_customer_support@gmail.com",
    date_of_birth = "1990-01-01",
    username = "test_customer_support00192",
    role = "customer_support",
    address = "near park golden st.1/23",
    state = "new york",
    country = "usa",
    zip_code = int(10001),
    password = "test_password"
    ):
        customer_support = CustomerSupport(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            username=username,
            role=role,
            address=address,
            state=state,
            country=country,
            zip_code=zip_code
        )
        customer_support.customer_support_password(password)
        db.session.add(customer_support)
        db.session.commit()
        return customer_support
    return register_customer_support

@pytest.fixture
def create_employee(db):
    def register_employee(

    full_name = "test employee",
    phone_number = int(1234567890),
    email = "test_employee@gmail.com",
    date_of_birth = "1990-01-01",
    username = "test_employee00192",
    role = "employee",
    address = "near park golden st.1/23",
    state = "new york",
    country = "usa",
    zip_code = int(10001),
    password = "test_password"
    ):
        employee = Employee(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            username=username,
            role=role,
            address=address,
            state=state,
            country=country,
            zip_code=zip_code
        )
        employee.employee_password(password)
        db.session.add(employee)
        db.session.commit()
        return employee
    return register_employee

@pytest.fixture
def create_customer(db):
    def register_customer(

    full_name = "test customer",
    phone_number = int(1234567890),
    email = "test_customer@gmail.com",
    date_of_birth = "1990-01-01",
    username = "test_customer00192",
    role = "customer",
    address = "near park golden st.1/23",
    state = "new york",
    country = "usa",
    zip_code = int(10001),
    password = "test_password"
    ):
        customer = Customer(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            username=username,
            role=role,
            address=address,
            state=state,
            country=country,
            zip_code=zip_code
        )
        customer.customer_password(password)
        db.session.add(customer)
        db.session.commit()
        return customer
    return register_customer

@pytest.fixture
def admin_token(
    app,
    create_admin
):

    admin = create_admin()
    with app.app_context():
        access_token = create_access_token(
            identity=admin.id
        )
    return admin, access_token

@pytest.fixture
def manager_token(
    app,
    create_manager
):

    manager = create_manager()
    with app.app_context():
        access_token = create_access_token(
            identity=manager.id
        )
    return manager, access_token

@pytest.fixture
def customer_support_token(
    app,
    create_customer_support
):

    customer_support = create_customer_support()
    with app.app_context():
        access_token = create_access_token(
            identity=customer_support.id
        )
    return customer_support, access_token

@pytest.fixture
def employee_token(
    app,
    create_employee
):

    employee = create_employee()
    with app.app_context():
        access_token = create_access_token(
            identity=employee.id
        )
    return employee, access_token

@pytest.fixture
def customer_token(
    app,
    create_customer
):

    customer = create_customer()
    with app.app_context():
        access_token = create_access_token(
            identity=customer.id
        )
    return customer, access_token

def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }