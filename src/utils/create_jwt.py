import os
from datetime import datetime, timedelta

import jwt

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def create_access_token(payload):
    expire = datetime.utcnow() + timedelta(minutes=180)
    payload.update({"exp": expire})
    encoded_token = jwt.encode(payload, JWT_SECRET_KEY, ALGORITHM)
    # return f"Bearer {encoded_token}"
    return encoded_token
