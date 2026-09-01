def test_registration(client):
    response = client.post(
        "/api/manager/register",
        json={            
            "full_name" : "test User",
            "phone_number" : "9876543210",
            "email" : "test005@gmail.com",
            "password" : "123456",
            "date_of_birth" : "2000-05-15",
            "username" : "testuser123",
            "address" : "chennai",
            "state" : "Tamil Nadu",
            "country" : "india",
            "zip_code" : 12343
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Manager created successfully!"