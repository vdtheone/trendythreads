from flask import jsonify, request

from src.common_crud.crud import CRUD
from src.database import db
from src.models.inventory import Inventory

inventory_crud = CRUD(Inventory)


def add_product_stock():
    user_input_data = request.json
    product_in_inventory = (
        db.session.query(Inventory)
        .filter(Inventory.product_id == user_input_data["product_id"])
        .first()
    )
    if not product_in_inventory:
        responce = inventory_crud.create(user_input_data)
        return responce
    else:
        return jsonify(
            {"error": "Product is already in Inventory.So update the stock if you want"}
        )


def get_all_item():
    return inventory_crud.list_all()


def delete_item_from_inventory(inventory_item_id):
    return inventory_crud.delete(inventory_item_id)


def update_inventory_item(inventory_item_id):
    updated_data = request.json
    return inventory_crud.update(inventory_item_id, updated_data)
