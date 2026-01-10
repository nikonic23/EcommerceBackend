from tests.helpers import login

def test_place_order_empty_cart(client):
    login(client)

    response = client.post("/api/orders/place")
    assert response.status_code == 400