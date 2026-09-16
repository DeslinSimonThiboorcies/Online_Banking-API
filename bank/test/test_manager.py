from bank.test.conftest import auth_headers

REGISTER_URL = '/api/manager/register'
LOGIN_URI = '/api/manager/login'
VIEW_MANAGERS = '/api/manager/profiles'

def view_manager_url(manager_id):
    return f"/api/manager/profile/{manager_id}"

def update_manager_url(manager_id):
    return f'/api/manager/update/{manager_id}'

def delete_manager_url(manager_id):
    return f'/api/manager/delete/{manager_id}'

class TestManagerRegister:

    def test_register(
        self,
        client,
    ):
        response = client.post(
            REGISTER_URL,
            json={
            "full_name" : "test manager",
            "phone_number" : int(1234567891),
            "email" : "testmanager005@gmail.com",
            "password" : "pasw123456",
            "date_of_birth" : "2000-05-15",
            "username" : "test_manager00192",
            "address" : "near park golden st.1/23",
            "state" : "New York",
            "country" : "usa",
            "zip_code" : int(10001)
            }
        )
        assert response.status_code == 201
        assert response.get_json()["message"] == "Manager created successfully!"

    def test_register_duplicate_manager(
        self,
        client,
        create_manager
    ):
        create_manager(
            username = "duplicate_manager",
        )
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "Duplicate Manager",
                "phone_number": 1234567891,
                "email": "duplicatemanager@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "duplicate_manager",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001
            }
        )
        assert response.status_code == 400
        assert response.get_json()["message"] == "MANAGER ALREADY EXIST"


class TestManagerLogin:

    def test_login(
        self,
        client,
        create_manager
    ):
        create_manager(
            username = "login_manager123",
            password = "pasw123456"
        )
        response = client.post(
            LOGIN_URI,
            json={
                "username": "login_manager123",
                "password": "pasw123456"
            }
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body["Message"] == "Login Successfull"
        assert body ["Bearer"]

    def test_login_wrong_password(
            self,
            client,
            create_manager
        ):
        create_manager(
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

class TestManagerProfile:
    def test_manager_profile(
        self, 
        client
    ):
        response = client.get(VIEW_MANAGERS)
        assert response.status_code == 401

    def test_plain_manager(
        self,
        client,
        manager_token
        ):

        manager, token = manager_token
        response = client.get(
            view_manager_url(manager.id),
            headers=auth_headers(token)
        )
        assert response.status_code == 200

    def test_admin_allowed_(
        self, 
        app, 
        client, 
        admin_token, 
        create_manager
        ):

        admin, token = admin_token
        target_manager = create_manager(
            username="target_manager_user",
            email="target_manager@gmail.com",
            phone_number=1234567891,
        )
        response = client.get(
            view_manager_url(target_manager.id),
            headers=auth_headers(token)
        )
        assert response.status_code == 200
        assert response.get_json()["Message"]

class TestUpdateAdmin:

    def test_update_manager(
        self,
        client,
        manager_token,
    ):
        manager, token = manager_token

        response = client.put(
            update_manager_url(manager.id),
            json={"full_name": "Updated manager"},
            headers=auth_headers(token)
        )
        assert response.status_code == 200
        assert response.get_json()["Message"] == "Manager update successfull!"
                      
    def test_update_role_access(
        self,
        client,
        manager_token,
        create_manager
    ):
        manager, token = manager_token
        others = create_manager(username = "newusers")

        response = client.put(
            update_manager_url(others.id),
            json={"full_name": "testusername"},
            headers=auth_headers(token)
        )
        assert response.status_code == 403

    def test_update_Manager_target(
        self,
        client,
        manager_token,
        create_manager,
        db
    ):
        manager, token = manager_token
        target = create_manager(
            username = "targetuser",
            email = "traget@gmail.com",
            phone_number = 1234567893
        )

        response = client.put(
            update_manager_url(target.id),
            json={"full_name": "Updated by Admin"},
            headers=auth_headers(token)
        )

        assert response.status_code == 403

        db.session.refresh(target)
        assert target.full_name == "test manager"

    def test_update_manager_not_found(
        self,
        client,
        manager_token
    ):
        manager, token = manager_token

        response = client.put(
            update_manager_url(999),
            json={"full_name": "Non-existent manager"},
            headers=auth_headers(token)
        )

        assert response.status_code == 404


class TestDeleteAdmin:

    def test_delete_other_denied(
        self,
        client,
        manager_token,
        create_manager
    ):
        manager, token = manager_token
        other = create_manager(
            username = "otheruser",
            email="otheruser@gmail.com",
            phone_number=1234567892
        )
        response = client.delete(
            delete_manager_url(other.id),
            headers=auth_headers(token)
        )
        assert response.status_code == 403

    def test_manager_delete(
        self,
        client,
        manager_token
    ):
        manager, token = manager_token
        response = client.delete(
            delete_manager_url(99999999),
            headers=auth_headers(token)
        )

        assert response.status_code == 404