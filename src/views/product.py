from flask import jsonify, request
from fuzzywuzzy import fuzz

from src.database import db
from src.models.product import Product
from src.serializers.product_serializer import product_serializer


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


def one_product(product_id):
    product = db.session.query(Product).get(product_id)
    return jsonify(product_serializer(product).json)


# Normal search using query
# def search_product():
#     data = request.json
#     print(data["keyword"])
#     search_products = (
#         db.session.query(Product)
#         .filter(Product.name.contains(f"%{data['keyword']}%"))
#         .all()
#     )
#     all_products = [product_serializer(product).json for product in search_products]
#     return jsonify({"Products": all_products})


def search_product():
    query = request.args.get("query").lower()
    results = []
    products = db.session.query(Product).all()
    products = [product_serializer(all_product).json for all_product in products]

    filtered_products = [
        {
            "product": product,
            "score": fuzz.token_sort_ratio(query, product["name"].lower()),
        }
        for product in products
    ]

    # Filter products with a score greater than or equal to a threshold
    filtered_products = [item for item in filtered_products if item["score"] >= 15]

    # Sort the filtered products by score in descending order
    sorted_products = sorted(filtered_products, key=lambda x: x["score"], reverse=True)

    # Extract the product information (excluding the score)
    results = [item["product"] for item in sorted_products]

    return results
