from bank.test.conftest import auth_headers

REGISTER_URL = '/api/user/register'
LOGIN_URI = '/api/user/login'
VIEW_CUSTOMER_SERVICES = '/api/user/profile'


def view_customer_services_url(customer_services_id):
    return f"/api/user/my_profile/{customer_services_id}"


def update_customer_services_url(customer_services_id):
    return f'/api/user/update/my_profile/{customer_services_id}'


def delete_customer_services_url(customer_services_id):
    return f'/api/user/delete/my_profile/{customer_services_id}'


class TestCustomerServicesRegister:

    def test_register(self, client):
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "test customer support",
                "phone_number": 1234567891,
                "email": "customer_support_001@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "customer_support_001",
                "role": "customer_support",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001,
            },
        )
        assert response.status_code == 201
        assert response.get_json()["Message"] == "User create successfull!"

    def test_register_duplicate_user(self, client, create_customer_support):
        create_customer_support(username="duplicate_user")
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "Duplicate Customer Support",
                "phone_number": 1234567892,
                "email": "duplicatecustomer@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "duplicate_user",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001,
            },
        )
        assert response.status_code == 400
        assert response.get_json()["Message"] == "USER ALREADY EXIST"


class TestCustomerServicesLogin:

    def test_login(self, client, create_customer_support):
        create_customer_support(username="login_user", password="pasw123456")
        response = client.post(
            LOGIN_URI,
            json={
                "username": "login_user",
                "password": "pasw123456",
            },
        )
        assert response.status_code == 200
        body = response.get_json()
        assert "Bearer" in body

    def test_login_wrong_password(self, client, create_customer_support):
        create_customer_support(username="wrong_user", password="pasw12345")
        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrong_user",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 400

    def test_login_wrong_username(self, client):
        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrongusername",
                "password": "notsamepassword",
            },
        )
        assert response.status_code == 400


class TestCustomerServicesProfile:

    def test_customer_services_profile(self, client):
        response = client.get(VIEW_CUSTOMER_SERVICES)
        assert response.status_code == 401

    def test_plain_customer_service(self, client, customer_support_token):
        customer_support, token = customer_support_token
        response = client.get(
            view_customer_services_url(customer_support.id),
            headers=auth_headers(token),
        )
        assert response.status_code == 200

    def test_admin_allowed_(self, client, admin_token, create_customer_support):
        admin, token = admin_token
        target_customer_support = create_customer_support(
            username="target_customer_support_user",
            email="target_customer_support@gmail.com",
            phone_number=1234567891,
        )
        response = client.get(
            view_customer_services_url(target_customer_support.id),
            headers=auth_headers(token),
        )
        assert response.status_code == 200
        assert response.get_json()["Message"]


class TestUpdateCustomerServices:

    def test_update_customer_service(self, client, customer_support_token):
        customer_support, token = customer_support_token
        response = client.put(
            update_customer_services_url(customer_support.id),
            json={"full_name": "Updated customer support"},
            headers=auth_headers(token),
        )
        assert response.status_code == 200
        assert response.get_json()["Message"] == "User update successfull!"

    def test_update_role_access(self, client, customer_support_token, create_customer_support):
        customer_support, token = customer_support_token
        other = create_customer_support(username="other_customer_support")

        response = client.put(
            update_customer_services_url(other.id),
            json={"full_name": "New name"},
            headers=auth_headers(token),
        )
        assert response.status_code == 403

    def test_update_customer_service_target(self, client, customer_support_token, create_customer_support, db):
        customer_support, token = customer_support_token
        target = create_customer_support(
            username="target_customer_support",
            email="target_customer_support@gmail.com",
            phone_number=1234567893,
        )

        response = client.put(
            update_customer_services_url(target.id),
            json={"full_name": "Updated by Admin"},
            headers=auth_headers(token),
        )

        assert response.status_code == 403

        db.session.refresh(target)
        assert target.full_name == "test customer support"

    def test_update_customer_service_not_found(self, client, customer_support_token):
        customer_support, token = customer_support_token

        response = client.put(
            update_customer_services_url(999),
            json={"full_name": "Non-existent customer support"},
            headers=auth_headers(token),
        )

        assert response.status_code == 404


class TestDeleteCustomerServices:

    def test_delete_other_denied(self, client, customer_support_token, create_customer_support):
        customer_support, token = customer_support_token
        other = create_customer_support(username="other_customer_support_delete")
        response = client.put(
            delete_customer_services_url(other.id),
            headers=auth_headers(token),
        )
        assert response.status_code == 403

    def test_customer_service_delete(self, client, customer_support_token):
        customer_support, token = customer_support_token
        response = client.put(
            delete_customer_services_url(99999999),
            headers=auth_headers(token),
        )
        assert response.status_code == 404

    def test_manager_delete(self, client, manager_token):
        manager, token = manager_token
        response = client.put(
            delete_customer_services_url(99999999),
            headers=auth_headers(token)
        )

        assert response.status_code == 404
