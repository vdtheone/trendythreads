from datetime import datetime

from sqlalchemy import Column, DateTime, String

from src.database import db
from src.utils.generate_uuid import generate_uuid


class Category(db.Model):
    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
