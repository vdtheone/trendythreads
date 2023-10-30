from flask import jsonify, request

from src.database import db
from src.models.category import Category
from src.models.product import Product
from src.serializers.category_serializer import category_serializer
from src.serializers.product_serializer import product_serializer


def add_new_category():
    data = request.json
    new_cat = Category(name=data["name"], description=data["description"])
    db.session.add(new_cat)
    db.session.commit()
    db.session.refresh(new_cat)
    return jsonify({"message": "Add category"})


def all_categories():
    categories = db.session.query(Category).all()
    all_categories = [category_serializer(category).json for category in categories]
    return jsonify({"categories": all_categories})


def category_by_id(cat_id):
    category = db.session.query(Category).get(cat_id)
    return jsonify(category_serializer(category).json)


def products_by_category(cat_id):
    products = db.session.query(Product).filter(Product.category_id == cat_id).all()
    category = db.session.query(Category).get(cat_id)
    all_products = [product_serializer(product).json for product in products]
    return jsonify({"Category": category.name, "Products": all_products})
