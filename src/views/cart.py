from flask import request

from src.common_crud.crud import CRUD
from src.models.cart import Cart

cart_crud = CRUD(Cart)


def add_to_cart_item():
    data = request.json
    responce = cart_crud.create(data)
    return responce


def get_all_item():
    return cart_crud.list_all()


def delete_item_from_cart(cart_item_id):
    return cart_crud.delete(cart_item_id)


def update_cart_item(cart_item_id):
    updated_data = request.json
    return cart_crud.update(cart_item_id, updated_data)
