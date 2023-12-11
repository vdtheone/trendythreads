from flask import jsonify

from src.database import db
from src.models.category import Category
from src.models.inventory import Inventory


def product_serializer(product):
    return jsonify(
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "brand": product.brand,
            "image": product.image,
            "active": product.active,
            "category": {
                "category_id": product.category_id,
                "category_name": db.session.query(Category)
                .filter(Category.id == product.category_id)
                .first()
                .name,
            },
            "inventory": {
                "stock_status": "Stock available"
                if db.session.query(Inventory)
                .filter(Inventory.product_id == product.id)
                .first()
                .stock_quantity
                > 0
                else "Out of stock"
            },
        }
    )
