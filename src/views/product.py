from flask import jsonify, request

from src.database import db
from src.models.product import Product
from src.utils.product_serializer import product_serializer


def add_new_product():
    data = request.json
    new_product = Product(
        category_id=data["category_id"],
        name=data["name"],
        description=data["description"],
        price=data["price"],
        brand=data["brand"],
        stockquantity=data["stockquantity"],
        image=data["image"],
        active=data["active"],
    )
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)
    return jsonify({"message": "Product add successfully"})


def all_products():
    products = db.session.query(Product).all()
    all_products = [product_serializer(all_product).json for all_product in products]
    return jsonify({"Products": all_products})
