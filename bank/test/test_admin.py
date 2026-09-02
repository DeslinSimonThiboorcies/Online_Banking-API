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

class TestAdminLogin:

    def test_login(
        self,
        client,
        create_admin
    ):
        create_admin(
            username = "test_admin00192",
            password = "pasw123456"
        )
        response = client.post(
            LOGIN_URI,
            json={
                "username": "test_admin00192",
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
            username = "test_admin00192wrongadmin",
            password = "pasw12"
        )

        response = client.post(
            LOGIN_URI,
            json={
                "username": "test_admin00192wrongadmin",
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401

    def test_login_wrong_username(
        self,
        create_admin,
        client
    ):
        create_admin(
            username = "test_admin00192wrongadmin",
            password = "pasw12"
        )

        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrongusername",
                "password": "pasw12"
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

        token = admin_token
        response = client.get(
            VIEW_ADMIN,
            headers=auth_headers(token)
        )
        assert response.status_code == 403

    def admin_profile_with_token(
            self,
            client,
            admin_token,
            create_admin
    ):
        token = admin_token
        create_admin(
            username = "test_admin00192",
            password = "pasw123456"
        )
        response = client.get(
            VIEW_ADMIN,
            headers=auth_headers(token)
        )
        assert response.status_code == 200