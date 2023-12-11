import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import db
from src.models.product import Product


def generate_uuid():
    return str(uuid.uuid4())


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    product_id = Column(String, ForeignKey(Product.id))
    stock_quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    # Define a relationship with the Product table
    product = relationship('Product', backref='inventory')

    def serialize(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "stock_quantity": self.stock_quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
