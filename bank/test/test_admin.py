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
        