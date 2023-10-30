from flask import jsonify


def cart_serializer(cart):
    return jsonify(
        {
            "user_id": cart.user_id,
            "product_id": cart.product_id,
            "quantity": cart.quantity,
        }
    ).json
