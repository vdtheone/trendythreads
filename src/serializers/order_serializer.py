from flask import jsonify

from src.database import db
from src.models.order import Order
from src.models.product import Product


def order_serialzer(order):
    items = db.session.query(Product).join(Order, Product.id == order.product_id).all()
    items_serialized = []
    total_amount = 0
    for item in items:
        item_serialized = {
            "product_id": item.id,
            "name": item.name,
            "quantity": order.quantity,
            "price_per_unit": item.price,
            "total_price": order.quantity * item.price,
        }
        total_amount += item_serialized["total_price"]
        items_serialized.append(item_serialized)

    return jsonify(
        {
            "message": "Order placed successfully",
            "order_details": {
                "order_id": order.id,
                "user_id": order.user_id,
                "status": "Order placed",
                "items": items_serialized,
                "total_amount": total_amount,
            },
        }
    )
