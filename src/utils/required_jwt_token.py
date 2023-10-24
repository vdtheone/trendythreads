import os
from flask import jsonify, request
import jwt

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def login_required(func):
    def inner(*args, **kwargs):
        try:
            token = request.headers.get("Authorization")

            if not token:
                return jsonify({"error": "Token is missing"}), 401

            token_parts = token.split()

            token = token_parts[1]
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

            return func(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except:
            return jsonify({"error": "Internal server error"})

    return inner
