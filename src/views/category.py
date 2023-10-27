from flask import jsonify, request

from src.database import db
from src.models.category import Category


def add_new_category():
    data = request.json
    new_cat = Category(name=data["name"], description=data["description"])
    db.session.add(new_cat)
    db.session.commit()
    db.session.refresh(new_cat)
    return jsonify({"message": "Add category"})
