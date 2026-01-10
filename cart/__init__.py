from flask import Blueprint

cart_bp = Blueprint("cart", __name__)

from cart import routes