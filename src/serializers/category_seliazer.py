from flask import jsonify


def category_serializer(category):
    return jsonify({"name": category.name, "description": category.description})
