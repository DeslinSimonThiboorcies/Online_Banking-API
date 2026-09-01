from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import patch


def make_fake_admin(**overrides):
    defaults = dict(
        id=1,
        full_name="Deslin Simon",
        phone_number="9876543210",
        email="admin@bank.com",
        date_of_birth=date(1995, 1, 1),
        username="admin1",
        role="admin",
        address="Kanniyakumari",
        state="Tamil Nadu",
        country="India",
        zip_code="629001",
        created_at=datetime(2026, 1, 1, 10, 0, 0),
        login_at=datetime(2026, 1, 1, 10, 0, 0),
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)



# POST /api/admin/register

class TestRegister:
    def test_register_success(self, client):
        with patch("bank.routes.admin_route.AdminRegisterService") as mock_service:
            mock_service.register.return_value = None

            response = client.post("/api/admin/register", json={
                "full_name": "test User",
                "phone_number": "9876543210",
                "email": "test005@gmail.com",
                "password": "123456",
                "date_of_birth": "2000-05-15",
                "username": "testuser123",
                "address": "chennai",
                "state": "Tamil Nadu",
                "country": "india",
                "zip_code": "12343",
            })

        assert response.status_code == 201
        assert response.get_json()["message"] == "Admin created successfully!"
        mock_service.register.assert_called_once()

    def test_register_missing_body_returns_400(self, client):
        response = client.post(
            "/api/admin/register",
            data="not json",
            content_type="text/plain",
        )
        assert response.status_code == 400

    def test_register_duplicate_returns_400(self, client):
        with patch("bank.routes.admin_route.AdminRegisterService") as mock_service:
            mock_service.register.side_effect = ValueError("Username already exists.")

            response = client.post("/api/admin/register", json={
                "username": "testuser123",
                "email": "test005@gmail.com",
                "password": "123456",
            })

        assert response.status_code == 400
        assert "already exists" in response.get_json()["message"]


# POST /api/admin/login

class TestLogin:
    def test_login_success_returns_bearer_token(self, client):
        with patch("bank.routes.admin_route.AdminRegisterService") as mock_service:
            mock_service.login.return_value = "fake.jwt.token"

            response = client.post("/api/admin/login", json={
                "username": "testuser123",
                "password": "123456",
            })

        assert response.status_code == 200
        # Route currently returns the token under "Bearer", not "access_token"
        assert response.get_json()["Bearer"] == "fake.jwt.token"

    def test_login_invalid_credentials_returns_401(self, client):
        with patch("bank.routes.admin_route.AdminRegisterService") as mock_service:
            mock_service.login.side_effect = ValueError("Invalid credentials.")

            response = client.post("/api/admin/login", json={
                "username": "testuser123",
                "password": "wrong",
            })

        assert response.status_code == 401
        assert response.get_json()["message"] == "Invalid username or password."

    def test_login_missing_body_returns_400(self, client):
        response = client.post(
            "/api/admin/login",
            data="not json",
            content_type="text/plain",
        )
        assert response.status_code == 400


# GET /api/admin/profile

class TestProfile:
    def test_profile_requires_auth(self, client):
        response = client.get("/api/admin/profile")
        assert response.status_code == 401

    def test_profile_rejects_non_admin_role(self, client, customer_auth_header):
        response = client.get("/api/admin/profile", headers=customer_auth_header)
        assert response.status_code == 403
        assert response.get_json()["message"] == "Access denied!"

    def test_profile_returns_current_admin(self, client, auth_header):
        fake_admin = make_fake_admin()

        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = fake_admin

            response = client.get("/api/admin/profile", headers=auth_header)

        assert response.status_code == 200
        body = response.get_json()
        assert body["username"] == "testuser123" if False else body["username"] == "admin1"
        assert body["email"] == "admin@bank.com"
        # profile() looks up the CALLER's own record via the JWT identity
        mock_service.view_admin.assert_called_once_with("1")

    def test_profile_not_found_returns_404(self, client, auth_header):
        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = None

            response = client.get("/api/admin/profile", headers=auth_header)

        assert response.status_code == 404
        assert response.get_json()["message"] == "Admin not found!"


# PUT /api/admin/update/<admin_id>
class TestUpdate:
    def test_update_success(self, client, auth_header):
        fake_admin = make_fake_admin()

        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = fake_admin
            mock_service.update.return_value = None

            response = client.put(
                "/api/admin/update/1",
                json={"full_name": "Deslin S."},
                headers=auth_header,
            )

        assert response.status_code == 200
        mock_service.update.assert_called_once_with(fake_admin, {"full_name": "Deslin S."})

    def test_update_missing_body_returns_400(self, client, auth_header):
        """
        FAILS CURRENTLY: update_profile() returns jsonify({...}) with no
        status code when the body isn't JSON, so Flask defaults to 200.
        Add ", 400" to that return in admin_route.py to fix.
        """
        fake_admin = make_fake_admin()

        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = fake_admin

            response = client.put(
                "/api/admin/update/1",
                data="not json",
                content_type="text/plain",
                headers=auth_header,
            )

        assert response.status_code == 400

    def test_update_not_found_returns_404(self, client, auth_header):
        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = None

            response = client.put(
                "/api/admin/update/999",
                json={"full_name": "Nobody"},
                headers=auth_header,
            )

        assert response.status_code == 404

    def test_update_rejects_non_admin_role(self, client, customer_auth_header):
        response = client.put(
            "/api/admin/update/1",
            json={"full_name": "Hacker"},
            headers=customer_auth_header,
        )
        assert response.status_code == 403


# DELETE /api/admin/delete/<admin_id>
class TestDelete:
    def test_delete_success(self, client, auth_header):
        fake_admin = make_fake_admin()

        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = fake_admin
            mock_service.delete.return_value = None

            response = client.delete("/api/admin/delete/1", headers=auth_header)

        assert response.status_code == 200
        mock_service.delete.assert_called_once_with(fake_admin)

    def test_delete_not_found_returns_404_with_correct_message(self, client, auth_header):
        """
        FAILS CURRENTLY: the not-found branch in remove_admin() returns
        "Request body must be JSON." instead of "Admin not found!" -
        looks like a copy-paste from another route.
        """
        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = None

            response = client.delete("/api/admin/delete/999", headers=auth_header)

        assert response.status_code == 404
        assert response.get_json()["message"] == "Admin not found!"

    def test_delete_rejects_non_admin_role(self, client, customer_auth_header):
        """
        FAILS CURRENTLY: remove_admin() never calls require_admin_(), so
        any authenticated user - not just admins - can delete an admin
        account. Add the same "if not require_admin_(): ... 403" guard
        used in profile()/update_profile().
        """
        with patch("bank.routes.admin_route.AdminServices") as mock_service:
            mock_service.view_admin.return_value = make_fake_admin()

            response = client.delete("/api/admin/delete/1", headers=customer_auth_header)

        assert response.status_code == 403

    def test_delete_requires_auth(self, client):
        response = client.delete("/api/admin/delete/1")
        assert response.status_code == 401