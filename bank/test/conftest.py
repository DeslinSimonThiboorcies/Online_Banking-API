import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from bank.route.users_route.admin_route import admin_bp


@pytest.fixture
def app():
    
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        JWT_SECRET_KEY="test-secret-key",
    )

    JWTManager(app)
    app.register_blueprint(admin_bp, url_prefix="/api")

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_token(app):
    """A JWT carrying an admin role claim, matching what require_admin_()
    in admin_route.py checks for."""
    with app.app_context():
        return create_access_token(
            identity="1",
            additional_claims={"role": "admin"},
        )


@pytest.fixture
def customer_token(app):
    """A JWT for a non-admin caller, to confirm admin routes reject it."""
    with app.app_context():
        return create_access_token(
            identity="1",
            additional_claims={"role": "customer"},
        )


@pytest.fixture
def auth_header(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def customer_auth_header(customer_token):
    return {"Authorization": f"Bearer {customer_token}"}