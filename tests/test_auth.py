def test_register(client):
    response = client.post(
        "/register",
        data={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200


def test_login(client):
    response = client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
