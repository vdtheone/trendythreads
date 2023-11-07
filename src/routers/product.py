from flask import Blueprint

from src.views.product import (
    add_new_product,
    all_products,
    filter_product,
    one_product,
    product_pagination,
    product_rating_by_user,
    product_review_by_user,
    search_product,
)

product_bp = Blueprint("product", __name__)


@product_bp.route("/add_product", methods=["POST"])
def add_product():
    return add_new_product()


@product_bp.route("/all_products", methods=["GET"])
def get_all_products():
    return all_products()


# Pagination Using List Comprehension
@product_bp.route("/all_products_list_comprehension", methods=["GET"])
def get_all_products_list():
    return product_pagination()


@product_bp.route("/get_product_by_id/<product_id>", methods=["GET"])
def product_by_id(product_id):
    return one_product(product_id)


@product_bp.route("/search", methods=["GET"])
def search():
    return search_product()


@product_bp.route("/filter", methods=["GET"])
def filter():
    return filter_product()


@product_bp.route("/<product_id>/review", methods=["POST"])
def review_product(product_id):
    return product_review_by_user(product_id)


@product_bp.route("/<product_id>/rating", methods=["POST"])
def rating_product(product_id):
    return product_rating_by_user(product_id)
