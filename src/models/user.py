from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from src.database import db
from src.utils.generate_uuid import generate_uuid


class User(db.Model):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, default=generate_uuid())
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    mobile_no = Column(String)
    is_varify = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class EmailOTP(db.Model):
    __tablename__ = "emailotp"

    id = Column(String, primary_key=True, index=True, default=generate_uuid())
    userid = Column(String, ForeignKey(User.id))
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    otp = Column(Integer)
