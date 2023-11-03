from flask import Blueprint

from src.views.category import (
    add_new_category,
    all_categories,
    category_by_id,
    products_by_category,
)

category_bp = Blueprint("category", __name__)


@category_bp.route("/addcat", methods=["POST"])
def add_cat():
    return add_new_category()


@category_bp.route("/all_category", methods=["GET"])
def get_all_categories():
    return all_categories()


@category_bp.route("/<cat_id>", methods=["GET"])
def get_category_by_id(cat_id):
    return category_by_id(cat_id)


@category_bp.route("<cat_id>/products", methods=["GET"])
def get_products_by_category(cat_id):
    return products_by_category(cat_id)
