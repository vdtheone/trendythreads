from flask import Blueprint

from src.views.inventory import (
    add_product_stock,
    delete_item_from_inventory,
    get_all_item,
    update_inventory_item,
)

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/add_stock', methods=["POST"])
def product_stock():
    return add_product_stock()


@inventory_bp.route("/", methods=["GET"])
def all_inventory_item():
    return get_all_item()


@inventory_bp.route("/delete/<inventory_item_id>", methods=["DELETE"])
def delete_inventory_item(inventory_item_id):
    return delete_item_from_inventory(inventory_item_id)


@inventory_bp.route("/update/<inventory_item_id>", methods=["PATCH"])
def update_item_in_inventory(inventory_item_id):
    return update_inventory_item(inventory_item_id)
