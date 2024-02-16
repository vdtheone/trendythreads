from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import db
from src.models.product import Product
from src.models.user import User
from src.utils.generate_uuid import generate_uuid


class OrderStatus(str, Enum):
    ORDER_PLACED = "Order Placed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"
    ON_HOLD = "On Hold"
    PENDING_PAYMENT = "Pending Payment"
    RETURNED = "Returned"


# class Order(db.Model):
#     __tablename__ = "order"

#     id = Column(String, primary_key=True, index=True, default=generate_uuid)
#     user_id = Column(String, ForeignKey(User.id))
#     product_id = Column(String, ForeignKey(Product.id))
#     quantity = Column(Integer)
#     total_amount = Column(Integer)
#     status = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow())
#     updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

#     # Define relationships
#     user = relationship("User", back_populates="orders")
#     product = relationship("Product", back_populates="orders")

#     def serialize(self):
# return {
#     "id": self.id,
#     "user_id": self.user_id,
#     "product_id": self.product_id,
#     "quantity": self.quantity,
#     "total_amount": self.total_amount,
#     "created_at": self.created_at,
#     "updated_at": self.updated_at,
# }


class Order(db.Model):
    __tablename__ = "order"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey(User.id))
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    # Define relationships
    user = relationship("User", back_populates="orders")
    order_item = relationship("OrderItem", back_populates="orders")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class OrderItem(db.Model):
    __tablename__ = "orderitem"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    order_id = Column(String, ForeignKey(Order.id))
    product_id = Column(String, ForeignKey(Product.id))
    quantity = Column(Integer)
    total_amount = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    # Define relationships
    product = relationship("Product", back_populates="orders")
    orders = relationship("Order", back_populates="order_item")

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_amount": self.total_amount,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Invoice(db.Model):
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    order_id = Column(String, ForeignKey(Order.id))
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
