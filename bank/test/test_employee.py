from bank.test.conftest import auth_headers

REGISTER_URL = '/api/employee/register'
LOGIN_URI = '/api/employee/login'
VIEW_EMPLOYEES = '/api/employee/view_profile'

def view_employee_url(employee_id):
    return f"/api/employee/view_my_profile/{employee_id}"

def update_employee_url(employee_id):
    return f'/api/employee/upate/my_profile/{employee_id}'

def delete_employee_url(employee_id):
    return f'/api/employee/delete/my_profile/{employee_id}'


class TestEmployeeRegister:

    def test_register(self, client):
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "test employee",
                "phone_number": 1234567891,
                "email": "testemployee005@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "test_employee00192",
                "role": "cashier",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001,
            },
        )
        assert response.status_code == 201
        assert response.get_json()["Message"] == "Employee Created successfull!"

    def test_register_duplicate_employee(self, client, create_employee):
        create_employee(username="duplicate_employee")
        response = client.post(
            REGISTER_URL,
            json={
                "full_name": "Duplicate Employee",
                "phone_number": 1234567892,
                "email": "duplicateemployee@gmail.com",
                "password": "pasw123456",
                "date_of_birth": "2000-05-15",
                "username": "duplicate_employee",
                "address": "near park golden st.1/23",
                "state": "New York",
                "country": "usa",
                "zip_code": 10001,
            },
        )
        assert response.status_code == 400
        assert response.get_json()["Message"] == "EMPLOYEE ALREADY EXIST"


class TestEmployeeLogin:

    def test_login(self, client, create_employee):
        create_employee(username="login_employee123", password="pasw123456")
        response = client.post(
            LOGIN_URI,
            json={
                "username": "login_employee123",
                "password": "pasw123456",
            },
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body["Message"] == "Login Successfull"
        assert body["Bearer"]

    def test_login_wrong_password(self, client, create_employee):
        create_employee(username="wrong_employee", password="pasw12345")
        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrong_employee",
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    def test_login_wrong_username(self, client):
        response = client.post(
            LOGIN_URI,
            json={
                "username": "wrongusername",
                "password": "notsamepassword",
            },
        )
        assert response.status_code == 401


class TestEmployeeProfile:

    def test_employee_profile(self, client):
        response = client.get(VIEW_EMPLOYEES)
        assert response.status_code == 401

    def test_plain_employee(self, client, employee_token):
        employee, token = employee_token
        response = client.get(
            view_employee_url(employee.id),
            headers=auth_headers(token),
        )
        assert response.status_code == 200

    def test_admin_allowed_(self, client, admin_token, create_employee):
        admin, token = admin_token
        target_employee = create_employee(
            username="target_employee_user",
            email="target_employee@gmail.com",
            phone_number=1234567891,
        )
        response = client.get(
            view_employee_url(target_employee.id),
            headers=auth_headers(token),
        )
        assert response.status_code == 200
        assert response.get_json()["Message"]


class TestUpdateEmployee:

    def test_update_employee(self, client, employee_token):
        employee, token = employee_token
        response = client.put(
            update_employee_url(employee.id),
            json={"full_name": "Updated employee"},
            headers=auth_headers(token),
        )
        assert response.status_code == 200
        assert response.get_json()["Message"] == "Employee Update succcessfull!"

    def test_update_role_access(self, client, employee_token, create_employee):
        employee, token = employee_token
        other = create_employee(username="other_employee")

        response = client.put(
            update_employee_url(other.id),
            json={"full_name": "New name"},
            headers=auth_headers(token),
        )
        assert response.status_code == 403

    def test_update_employee_target(self, client, employee_token, create_employee, db):
        employee, token = employee_token
        target = create_employee(
            username="target_employee",
            email="target_employee@gmail.com",
            phone_number=1234567893,
        )

        response = client.put(
            update_employee_url(target.id),
            json={"full_name": "Updated by Admin"},
            headers=auth_headers(token),
        )

        assert response.status_code == 403

        db.session.refresh(target)
        assert target.full_name == "test employee"

    def test_update_employee_not_found(self, client, employee_token):
        employee, token = employee_token

        response = client.put(
            update_employee_url(999),
            json={"full_name": "Non-existent employee"},
            headers=auth_headers(token),
        )

        assert response.status_code == 404


class TestDeleteEmployee:

    def test_delete_other_denied(self, client, employee_token, create_employee):
        employee, token = employee_token
        other = create_employee(username="other_employee_delete")
        response = client.delete(
            delete_employee_url(other.id),
            headers=auth_headers(token),
        )
        assert response.status_code == 403

    def test_employee_delete(self, client, employee_token):
        employee, token = employee_token
        response = client.delete(
            delete_employee_url(99999999),
            headers=auth_headers(token),
        )
        assert response.status_code == 404


    def test_manager_delete(
        self,
        client,
        manager_token
    ):
        manager, token = manager_token
        response = client.delete(
            delete_employee_url(99999999),
            headers=auth_headers(token)
        )

        assert response.status_code == 404