from flask import jsonify
from sqlalchemy.exc import IntegrityError

from src.database import db


class CRUD:
    def __init__(self, model):
        self.model = model

    def create(self, data):
        try:
            new_instance = self.model(**data)
            db.session.add(new_instance)
            db.session.commit()
            db.session.refresh(new_instance)
            return {"id": new_instance.id, "message": "Record created successfully"}
        except IntegrityError:
            db.session.rollback()
            return jsonify(
                {"error": "Record already exists or violates a unique constraint"}
            )

    def read(self, item_id, serialize):
        item = db.session.query(self.model).get(item_id)
        if not item:
            return jsonify({"error": f"{self.model.__name__} not found"})
        return jsonify(serialize(item))

    def update(self, item_id, data):
        item = db.session.query(self.model).get(item_id)
        if not item:
            return jsonify({"error": f"{self.model.__name__} not found"})
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        db.session.refresh(item)
        return jsonify({"message": f"{self.model.__name__} updated"})

    def delete(self, item_id):
        item = db.session.query(self.model).get(item_id)
        if not item:
            return jsonify({"error": f"{self.model.__name__} not found"})
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": f"{self.model.__name__} deleted"})

    def list_all(self):
        items = db.session.query(self.model).all()
        if not items:
            return jsonify({"error": f"No {self.model.__name__} found"})
        return jsonify([item.serialize() for item in items])
