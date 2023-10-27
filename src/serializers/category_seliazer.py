from flask import jsonify


def category_serializer(category):
    return jsonify(
        {"id": category.id, "name": category.name, "description": category.description}
    )
