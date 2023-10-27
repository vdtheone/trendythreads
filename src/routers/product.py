from flask import Blueprint

from src.views.product import add_new_product, all_products, one_product, search_product

product_bp = Blueprint("product", __name__)


@product_bp.route("/add_product", methods=["POST"])
def add_product():
    return add_new_product()


@product_bp.route("/all_products", methods=["GET"])
def get_all_products():
    return all_products()


@product_bp.route("/<product_id>", methods={"GET"})
def product_by_id(product_id):
    return one_product(product_id)


@product_bp.route("/search", methods=["GET"])
def search():
    return search_product()
