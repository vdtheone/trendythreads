from flask import jsonify, request

from src.database import db
from src.models.category import Category
from src.models.product import Product
from src.serializers.category_serializer import category_serializer
from src.serializers.product_serializer import product_serializer


# Add a new category to the database
def add_new_category():
    data = request.json
    new_cat = Category(name=data["name"], description=data["description"])
    db.session.add(new_cat)
    db.session.commit()
    db.session.refresh(new_cat)
    return jsonify({"message": "Add category"})


# Retrieve all categories from the database
def all_categories():
    categories = db.session.query(Category).all()
    all_categories = [category_serializer(category).json for category in categories]
    return jsonify({"categories": all_categories})


# Retrieve a category by its ID
def category_by_id(cat_id):
    category = db.session.query(Category).get(cat_id)
    if not category:
        return jsonify({"error": "Category not found"})
    return jsonify(category_serializer(category).json)


# Retrieve products associated with a category by its name
def products_by_category(cat_name):
    category = (
        db.session.query(Category).filter(Category.name.ilike(f"%{cat_name}%")).first()
    )
    if not category:
        return jsonify({"error": "Category not found"})
    products = (
        db.session.query(Product).filter(Product.category_id == category.id).all()
    )
    category = db.session.query(Category).get(category.id)
    all_products = [product_serializer(product).json for product in products]
    return jsonify({"Category": category.name, "Products": all_products})
