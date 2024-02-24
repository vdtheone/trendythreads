from src.database import db
from src.models.order import OrderItem


def add_new_order_serialzer(order_object):
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

    return {
        "message": "Order placed successfully",
        "order_details": {
            "order_id": order_object.id,
            "user_id": order_object.user_id,
            "status": "Order placed",
            "products": products_serialized,
            "total_amount": total_amount,
        },
    }


def all_customer_orders_serialzer(order_object):
    products_serialized = []
    total_amount = 0
    serialized = {
        "product_id": order_object.product.id,
        "name": order_object.product.name,
        "description": order_object.product.description,
        "price": order_object.product.price,
        "brand": order_object.product.brand,
        "image": order_object.product.image,
        "quantity": order_object.quantity,
        "price_per_unit": order_object.product.price,
        "total_price": order_object.quantity * order_object.product.price,
    }
    total_amount += order_object.product.price * order_object.quantity
    products_serialized.append(serialized)

    return {
        "order_details": {
            "order_id": order_object.order_id,
            "total_amount": total_amount,
            "product": serialized,
            "total_amount": total_amount,
            "created_at": order_object.created_at,
            "updated_at": order_object.updated_at,
        },
    }


# data = {
#     "orders": [
#         {
#             "id": 1,
#             "customer_name": "John Doe",
#             "total_amount": 50.00,
#             "items": [
#                 {"id": 101, "name": "Product 1", "price": 20.00, "quantity": 2},
#                 {"id": 102, "name": "Product 2", "price": 10.00, "quantity": 1},
#             ],
#         }
#     ]
# }
