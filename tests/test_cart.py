from tests.helpers import login

def test_add_to_cart(client):
    login(client)

    response = client.post(
        "/api/cart/add",
        data={"product_id": 1, "quantity": 1},
        follow_redirects=True
    )

    assert response.status_code == 200
