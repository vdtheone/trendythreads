from flask import Blueprint

from src.views.product import add_new_product, all_products

product_bp = Blueprint("product", __name__)


@product_bp.route("/addproduct", methods=["POST"])
def add_product():
    return add_new_product()


@product_bp.route("/", methods=["GET"])
def get_all_products():
    return all_products()
