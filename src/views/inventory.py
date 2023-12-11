from flask import request

from src.common_crud.crud import CRUD
from src.models.inventory import Inventory

inventory_crud = CRUD(Inventory)


def add_product_stock():
    data = request.json
    responce = inventory_crud.create(data)
    return responce


def get_all_item():
    return inventory_crud.list_all()


def delete_item_from_inventory(inventory_item_id):
    return inventory_crud.delete(inventory_item_id)


def update_inventory_item(inventory_item_id):
    updated_data = request.json
    return inventory_crud.update(inventory_item_id, updated_data)
