import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import db
from src.models.category import Category
from src.models.user import User


def generate_uuid():
    return str(uuid.uuid4())


class Product(db.Model):
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    category_id = Column(String, ForeignKey(Category.id))
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    brand = Column(String)
    stockquantity = Column(Integer)
    image = Column(String)
    active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    # Define one-to-many relationship with orders
    orders = relationship("Order", back_populates="product")

    def product_serializer(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "brand": self.brand,
            "stockquantity": self.stockquantity,
            "image": self.image,
            "active": self.active,
        }


class RatingAndReview(db.Model):
    __tablename__ = "rating_and_reviews"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey(User.id))
    product_id = Column(String, ForeignKey(Product.id))
    rating = Column(Float, default=0)
    review_message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "review_message": self.review_message,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
