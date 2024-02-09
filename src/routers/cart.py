from flask import Blueprint

from src.views.cart import (
    add_to_cart_item,
    delete_all_items,
    delete_item_from_cart,
    get_all_item,
    get_cart_count,
    update_cart_item,
)

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("add_to_cart", methods=["POST"])
def add_to_cart():
    return add_to_cart_item()


@cart_bp.route("/", methods=["GET"])
def all_cart_item():
    return get_all_item()


@cart_bp.route("/<cart_item_id>", methods=["DELETE"])
def delete(cart_item_id):
    return delete_item_from_cart(cart_item_id)


@cart_bp.route("<cart_item_id>", methods=["PATCH"])
def update_item_in_cart(cart_item_id):
    return update_cart_item(cart_item_id)


@cart_bp.route("/delete-all-items", methods=['DELETE'])
def delete_all_cart_items():
    return delete_all_items()


@cart_bp.route('/count', methods=['GET'])
def cart_count():
    return get_cart_count()
