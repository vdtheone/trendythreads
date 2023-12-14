from flask import jsonify, request
from fuzzywuzzy import fuzz

from src.common_crud.crud import CRUD
from src.database import db
from src.models.product import Product, RatingAndReview
from src.serializers.product_serializer import product_serializer
from src.utils.required_jwt_token import token_required

product_crud = CRUD(Product)


def add_new_product():
    data = request.json
    new_product = Product(
        category_id=data["category_id"],
        name=data["name"],
        description=data["description"],
        price=data["price"],
        brand=data["brand"],
        image=data["image"],
        active=data["active"],
    )
    db.session.add(new_product)
    db.session.commit()
    db.session.refresh(new_product)
    return jsonify({"message": "Product add successfully"})


def all_products():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    offset_val = (page - 1) * limit

    products_query = db.session.query(Product)
    all_products_length = products_query.count()
    all_products = products_query.limit(limit).offset(offset_val).all()

    limited_products = [product_serializer(product).json for product in all_products]

    return jsonify(
        {
            "data": limited_products,
            "count": all_products_length,
            # "a_No_of_products": len(limited_products),
            # "a_no_of_pages": ceil(all_products_length / limit),
            # "a_offset_val": offset_val,
            # "a_currunt_page_no": page,
        }
    )


def one_product(product_id):
    product = db.session.query(Product).get(product_id)
    if not product:
        return jsonify({"error": "Product not found"})
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
    search_value = request.args.get("query").lower()
    results = []
    products = db.session.query(Product).all()
    products = [product_serializer(all_product).json for all_product in products]

    filtered_products = [
        {
            "product": product,
            "score": fuzz.token_sort_ratio(search_value, product["name"].lower()),
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


def filter_product():
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    brand = request.args.get("brand")

    products = db.session.query(Product)

    if min_price:
        products = products.filter(Product.price >= float(min_price))

    if max_price:
        products = products.filter(Product.price <= float(max_price))

    if brand:
        products = products.filter(Product.brand == brand)

    # Execute the query and retrieve the filtered products
    filtered_products = products.all()

    all_products = [
        product_serializer(all_product).json for all_product in filtered_products
    ]

    return jsonify({"Products": all_products})


@token_required
def product_review_by_user(decoded_data, product_id):
    # check product is exist  or not
    product = db.session.query(Product).get(product_id)
    if not product:
        return jsonify({"error": "Product not found"})

    user_id = decoded_data["id"]
    review_data = request.json
    user_id_and_product_id = {"user_id": user_id, "product_id": product_id}
    review_data.update(user_id_and_product_id)
    review = RatingAndReview(**review_data)
    db.session.add(review)
    db.session.commit()
    db.session.refresh(review)
    return jsonify({"message": "user reviewed product"})


@token_required
def product_rating_by_user(decoded_data, product_id):
    # check product is exist  or not
    product = db.session.query(Product).get(product_id)
    if not product:
        return jsonify({"error": "Product not found"})

    user_id = decoded_data["id"]
    review_data = request.json
    user_id_and_product_id = {"user_id": user_id, "product_id": product_id}
    review_data.update(user_id_and_product_id)
    review = RatingAndReview(**review_data)
    db.session.add(review)
    db.session.commit()
    db.session.refresh(review)
    return jsonify({"message": "user rating a product"})


# Pagination Using List Comprehension
def product_pagination():
    all_products = db.session.query(Product).all()

    # Define the page size (number of items per page)
    limit = int(request.args.get("limit", 10))

    # Define the current page number
    page = int(request.args.get("page", 1))

    # Calculate the starting and ending indices for the current page
    start_index = (page - 1) * limit
    end_index = page * limit

    # Retrieve the data for the current page
    page_data = all_products[start_index:end_index]
    return jsonify(
        {
            "data": [product_serializer(product).json for product in page_data],
            "count": len(all_products),
        }
    )
