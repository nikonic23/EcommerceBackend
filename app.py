from flask import Flask, session, request, g
import uuid
from config import Config
from extensions import mysql, jwt
from auth import auth_bp
from main import main_bp
from admin import admin_bp
from products import products_bp
from cart import cart_bp
from orders import orders_bp
from utils.security import set_secuirty_headers
from utils.request_id import generate_request_id
from utils.logger import setup_logger


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    jwt.init_app(app)

    return app

app = create_app()


app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)


@app.before_request
def attach_jwt():
    token = session.get('access_token')
    if token:
        request.headers.environ['HTTP_AUTHORIZATION'] = f'Bearer {token}'

logger = setup_logger()
@app.before_request
def attach_request_id():
    g.request_id = str(uuid.uuid4())
    logger.info(f"request_id={g.request_id} path={request.path}")

@app.after_request
def apply_security_headers(response):
    return set_secuirty_headers(response)


@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception")
    return {"msg": "Internal server error"}, 500

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return {"msg": "Token expired, please login again"}, 401


if __name__ == '__main__':
    app.run (debug = True)