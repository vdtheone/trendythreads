from flask import jsonify, request

from src.common_crud.crud import CRUD
from src.database import db
from src.models.inventory import Inventory

inventory_crud = CRUD(Inventory)


# Function to add product stock to the inventory
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
        error_message = (
            "Product is already in Inventory. So update the stock if you want"
        )
        return jsonify({"error": error_message})


# Function to get all items from the inventory
def get_all_item():
    return inventory_crud.list_all()


# Function to delete an item from the inventory by ID
def delete_item_from_inventory(inventory_item_id):
    return inventory_crud.delete(inventory_item_id)


# Function to update an item in the inventory by ID
def update_inventory_item(inventory_item_id):
    updated_data = request.json
    return inventory_crud.update(inventory_item_id, updated_data)
