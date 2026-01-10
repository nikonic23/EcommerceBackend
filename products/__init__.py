from flask import Blueprint

products_bp = Blueprint("products", __name__)

from products import routes