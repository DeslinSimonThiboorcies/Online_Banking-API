from bank.model.users_model import admin
from bank.test.conftest import auth_headers

REGISTER_URL = '/api/admin/register'
LOGIN_URI = '/api/admin/login'
VIEW_ADMIN = '/api/admin/profile'

def update_admin_url(admin_id):
    return f'/api/admin/update/{admin_id}'

def delete_admin_url(admin_id):
    return f'/api/admin/delete/{admin_id}'


class TestAdminRegister:

    def test_register(
        self,
        client,
    ):
        response = client.post(
            REGISTER_URL,
            json={
            "full_name" : "test admin",
            "phone_number" : int(1234567890),
            "email" : "testadmin005@gmail.com",
            "password" : "pasw123456",
            "date_of_birth" : "2000-05-15",
            "username" : "test_admin00192",
            "address" : "near park golden st.1/23",
            "state" : "New York",
            "country" : "usa",
            "zip_code" : int(10001)
            }
        )
        assert response.status_code == 201
        assert response.get_json()["message"] == "Admin created successfully!"


    def test_register_duplicate_admin(
        self,
        client,
        create_admin
    ):
        create_admin(
            username = "duplicate_admin",
        )
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "Duplicate Admin",
                "phone_number": 1234567890,
                "email": "duplicateadmin@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "duplicate_admin",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001
            }
        )
        assert response.status_code == 400
        assert response.get_json()["message"] == "ADMIN ALREADY EXIST"


class TestAdminLogin:

    def test_login(
        self,
        client,
        create_admin
    ):
        create_admin(
            username = "login_admin123",
            password = "pasw123456"
        )
        response = client.post(
            LOGIN_URI,
            json={
                "username": "login_admin123",
                "password": "pasw123456"
            }
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body["message"] == "Login successful!"
        assert body ["Bearer"]

    def test_login_wrong_password(
            self,
            client,
            create_admin
        ):
        create_admin(
            username = "wrong_users",
            password = "pasw12345"
        )

        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrong_users",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401

    def test_login_wrong_username(
        self,
        client
    ):
        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrongusername",
                "password": "notsamepassword"
            }
        )

        assert response.status_code == 401


class TestAdminProfile:

    def test_admin_profile(self, client):
        response = client.get(VIEW_ADMIN)
        assert response.status_code == 401

    def test_plain_admin(
        self,
        client,
        admin_token
        ):

        admin, token = admin_token
        response = client.get(
            VIEW_ADMIN,
            headers=auth_headers(token)
        )
        assert response.status_code == 200

    def test_admin_allowed(self, app, client, admin_token, create_admin):
        admin, token = admin_token
        other_admin = create_admin(
            username="other_admin_user",
            email="other_admin@gmail.com",
            phone_number=1234567891,
            password="newpassword123"
        )
        response = client.get(
            VIEW_ADMIN,
            headers=auth_headers(token)
        )
        assert response.status_code == 200
        assert response.get_json()["Message"]


class TestUpdateAdmin:

    def test_update_admin(
        self,
        client,
        admin_token,
    ):
        admin, token = admin_token

        response = client.put(
            update_admin_url(admin.id),
            json={"full_name": "Updated Admin"},
            headers=auth_headers(token)
        )
        assert response.status_code == 200
        assert response.get_json()["message"] == "Admin updated successfully"

    def test_update_role_access(
        self,
        client,
        admin_token,
        create_admin
    ):
        admin, token = admin_token
        others = create_admin(username = "newusers")

        response = client.put(
            update_admin_url(others.id),
            json={"full_name": "testusername"},
            headers=auth_headers(token)
        )
        assert response.status_code == 403

    def test_update_admin_target(
        self,
        client,
        admin_token,
        create_admin,
        db
    ):
        admin, token = admin_token
        target = create_admin(
            username = "targetuser",
            email = "target@gmail.com",
            phone_number = 1234567893
        )

        response = client.put(
            update_admin_url(target.id),
            json={"full_name": "Updated by Admin"},
            headers=auth_headers(token)
        )

        assert response.status_code == 200

        db.session.refresh(target)
        db.session.refresh(admin)
        assert target.full_name == "Updated by Admin"
        assert admin.full_name != "Updated by Admin"

    def test_update_admin_not_found(
        self,
        client,
        admin_token
    ):
        admin, token = admin_token

        response = client.put(
            update_admin_url(999),
            json={"full_name": "Non-existent Admin"},
            headers=auth_headers(token)
        )

        assert response.status_code == 404


class TestDeleteAdmin:

    def test_delete_other_denied(
        self,
        client,
        admin_token,
        create_admin
    ):
        admin, token = admin_token
        other = create_admin(
            username = "otheruser",
            email="otheruser@gmail.com",
            phone_number=1234567892
        )
        response = client.delete(
            delete_admin_url(other.id),
            headers=auth_headers(token)
        )
        assert response.status_code == 403

    def test_admin_delete(
        self,
        client,
        admin_token
    ):
        admin, token = admin_token
        response = client.delete(
            delete_admin_url(99999999),
            headers=auth_headers(token)
        )

        assert response.status_code == 404