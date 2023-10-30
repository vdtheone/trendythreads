import os

import jwt
from flask import jsonify, request

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

        except jwt.exceptions.DecodeError:
            return jsonify({"error": "Not enough segments provided in token"})

        except Exception:
            return jsonify({"error": "Internal server error"})

    return inner
