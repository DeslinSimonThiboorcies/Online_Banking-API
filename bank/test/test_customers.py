from bank.test.conftest import auth_headers

REGISTER_URL = "/api/customer/register"
LOGIN_URL = "/api/customer/login"
VIEW_CUSTOMERS = "/api/customer/profile"


def view_customer_url(customer_id):
    return f"/api/customer/my_profile/{customer_id}"


def update_customer_url(customer_id):
    return f"/api/customer/update/my_profile/{customer_id}"


def delete_customer_url(customer_id):
    return f"/api/customer/delete/my_profile/{customer_id}"


class TestCustomerRegister:

    def test_register(self, client):
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "test customer",
                "phone_number": 1234567891,
                "email": "testcustomer005@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "test_customer00192",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001,
            },
        )
        assert response.status_code == 201
        assert response.get_json()["Message"] == "User create successfull!"

    def test_register_duplicate_customer(self, client, create_customer):
        create_customer(username="duplicate_customer")
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "Duplicate Customer",
                "phone_number": 1234567892,
                "email": "duplicatecustomer@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "duplicate_customer",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001,
            },
        )
        assert response.status_code == 400
        assert response.get_json()["Message"] == "USER ALREADY EXIST"


class TestCustomerLogin:

    def test_login(self, client, create_customer):
        create_customer(username="login_customer", password="pasw123456")
        response = client.post(
            LOGIN_URL,
            json={"username": "login_customer", "password": "pasw123456"},
        )
        assert response.status_code == 200
        assert response.get_json()["Bearer"]

    def test_login_wrong_password(self, client, create_customer):
        create_customer(username="wrong_customer", password="pasw12345")
        response = client.post(
            LOGIN_URL,
            json={"username": "wrong_customer", "password": "wrongpassword"},
        )
        assert response.status_code == 400

    def test_login_wrong_username(self, client):
        response = client.post(
            LOGIN_URL,
            json={"username": "wrongusername", "password": "notsamepassword"},
        )
        assert response.status_code == 400


class TestCustomerProfile:

    def test_customer_profile_requires_authentication(self, client):
        response = client.get(VIEW_CUSTOMERS)
        assert response.status_code == 401

    def test_plain_customer(self, client, customer_token):
        customer, token = customer_token
        response = client.get(
            view_customer_url(customer.id), headers=auth_headers(token)
        )
        assert response.status_code == 200

    def test_admin_allowed(self, client, admin_token, create_customer):
        _, token = admin_token
        target = create_customer(
            username="target_customer_user",
            email="target_customer@gmail.com",
            phone_number=1234567893,
        )
        response = client.get(
            view_customer_url(target.id), headers=auth_headers(token)
        )
        assert response.status_code == 200
        assert response.get_json()["Message"]


class TestUpdateCustomer:

    def test_update_customer(self, client, customer_token):
        customer, token = customer_token
        response = client.put(
            update_customer_url(customer.id),
            json={"full_name": "Updated customer"},
            headers=auth_headers(token),
        )
        assert response.status_code == 200
        assert response.get_json()["Message"] == "customer update successfull!"

    def test_update_role_access(self, client, customer_token, create_customer):
        _, token = customer_token
        other = create_customer(username="other_customer")
        response = client.put(
            update_customer_url(other.id),
            json={"full_name": "New name"},
            headers=auth_headers(token),
        )
        assert response.status_code == 403

    def test_update_customer_not_found(self, client, customer_token):
        _, token = customer_token
        response = client.put(
            update_customer_url(999),
            json={"full_name": "Non-existent customer"},
            headers=auth_headers(token),
        )
        assert response.status_code == 404


class TestDeleteCustomer:

    def test_delete_other_denied(self, client, customer_token, create_customer):
        _, token = customer_token
        other = create_customer(username="other_customer_delete")
        response = client.put(
            delete_customer_url(other.id), headers=auth_headers(token)
        )
        assert response.status_code == 403

    def test_customer_delete_not_found(self, client, customer_token):
        _, token = customer_token
        response = client.put(
            delete_customer_url(99999999), headers=auth_headers(token)
        )
        assert response.status_code == 404

    def test_manager_delete_not_found(self, client, manager_token):
        _, token = manager_token
        response = client.put(
            delete_customer_url(99999999), headers=auth_headers(token)
        )
        assert response.status_code == 404
