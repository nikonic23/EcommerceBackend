import pytest
from app import app as flask_app
from extensions import mysql

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })

    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def app_with_error(app):
    @app.route("/test-error")
    def test_error():
        raise Exception("boom")

    return app

@pytest.fixture(autouse=True)
def clean_db():
    from utils.helpers import get_cursor
    from extensions import mysql

    cursor = get_cursor()
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM cart_items")
    cursor.execute("DELETE FROM carts")
    mysql.connection.commit()
    cursor.close()