from flask import jsonify

from src.database import db
from src.models.order import OrderItem


def order_serialzer(order_object):
    products = (
        db.session.query(OrderItem).filter(OrderItem.order_id == order_object.id).all()
    )
    products_serialized = []
    total_amount = 0
    for product in products:
        serialized = {
            "product_id": product.product.id,
            "name": product.product.name,
            "quantity": product.quantity,
            "price_per_unit": product.product.price,
            "total_price": product.quantity * product.product.price,
        }
        total_amount += product.product.price * product.quantity
        products_serialized.append(serialized)

    return jsonify(
        {
            "message": "Order placed successfully",
            "order_details": {
                "order_id": order_object.id,
                "user_id": order_object.user_id,
                "status": "Order placed",
                "products": products_serialized,
                "total_amount": total_amount,
            },
        }
    )
