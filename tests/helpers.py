def login(client):
    return client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "password123"
        },
        follow_redirects=True
    )