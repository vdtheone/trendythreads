from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from src.database import db
from src.models.product import Product
from src.models.user import User
from src.utils.generate_uuid import generate_uuid


class Cart(db.Model):
    __tablename__ = "cart"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey(User.id))
    product_id = Column(String, ForeignKey(Product.id))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def serialize(self):
        product = (
            db.session.query(Product).filter(Product.id == self.product_id).first()
        )

        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "name": product.name,
            "price": product.price,
            "brand": product.brand,
            "image": product.image,
        }
