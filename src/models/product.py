import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from src.database import db
from src.models.category import Category


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
