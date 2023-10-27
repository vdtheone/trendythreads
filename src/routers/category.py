from flask import Blueprint

from src.views.category import add_new_category

category_bp = Blueprint("category", __name__)


@category_bp.route("/addcat", methods=["POST"])
def add_cat():
    return add_new_category()
