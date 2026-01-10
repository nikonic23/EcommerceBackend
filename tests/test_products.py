from tests.helpers import login

def test_products_page(client):
    login(client)

    response = client.get("/products")
    assert response.status_code == 200
