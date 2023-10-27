from flask import jsonify


def product_serializer(product):
    return jsonify(
        {
            "category_id": product.category_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "brand": product.brand,
            "stockquantity": product.stockquantity,
            "image": product.image,
            "active": product.active,
        }
    )
