from sqlalchemy import Column, ForeignKey, Integer, String

from src.database import db
from src.models.user import User
from src.utils.generate_uuid import generate_uuid


class Address(db.Model):
    __tablename__ = "address"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(String, ForeignKey(User.id))
    first_name = Column(String)
    last_name = Column(String)
    mobile_no = Column(String)
    pincode = Column(Integer)
    address = Column(String)
    city_district_town = Column(String)
    state = Column(String)
    landmark = Column(String)
    alernate_mobile_no = Column(String)
    address_type = Column(String)

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mobile_no": self.mobile_no,
            "pincode": self.pincode,
            "address": self.address,
            "city_district_town": self.city_district_town,
            "state": self.state,
            "landmark": self.landmark,
            "alernate_mobile_no": self.alernate_mobile_no,
            "address_type": self.address_type,
        }
