from flask import g, jsonify, request

from src.common_crud.crud import CRUD
from src.database import db
from src.models.cart import Cart
from src.serializers.cart_serializer import cart_serializer
from src.utils.required_jwt_token import login_required, token_required

cart_crud = CRUD(Cart)


# Endpoint to add an item to the user's cart
@login_required
def add_to_cart_item():
    data = request.json
    data['user_id'] = g.user
    responce = cart_crud.create(data)
    return responce


# Endpoint to get all items in the user's cart
@login_required
def get_all_item():
    user_id = g.user
    items = db.session.query(Cart).filter_by(user_id=user_id).all()
    if not items:
        return jsonify({"error": "No Cart found"}), 404

    cart_items = [cart_serializer(item) for item in items]

    return jsonify(
        {
            "cart_items": cart_items,
            "total_items": len(cart_items),
            "total_cost": sum(item["price"] * item["quantity"] for item in cart_items),
        }
    )


# Endpoint to delete an item from the user's cart
def delete_item_from_cart(cart_item_id):
    return cart_crud.delete(cart_item_id)


# Endpoint to update an item in the user's cart
def update_cart_item(cart_item_id):
    updated_data = request.json
    return cart_crud.update(cart_item_id, updated_data)


# Endpoint to delete all items from the user's cart
@token_required
def delete_all_items(decoded_token):
    user_id = decoded_token.get("id")
    return cart_crud.delete_all(user_id)


# Endpoint to get the count of items in the user's cart
@login_required
def get_cart_count():
    user_id = g.user
    items = db.session.query(Cart).filter_by(user_id=user_id).all()
    cart_count = len(items)
    return jsonify({'cartCount': cart_count})


# Endpoint to get an item from the user's cart by its ID
@login_required
def get_cart_item_by_id(product_id):
    item = db.session.query(Cart).filter(Cart.product_id == product_id).first()
    if not item:
        return jsonify({"error": "No Cart found"}), 404
    return jsonify(item.serialize()), 200
