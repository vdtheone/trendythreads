import os
from functools import wraps

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

        except Exception as e:
            return jsonify({"error": str(e)})

    return inner


def decode_token(token):
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401

    except jwt.exceptions.DecodeError:
        return jsonify({"error": "Not enough segments provided in token"})

    except Exception:
        return jsonify({"error": "Internal server error from decorator"})


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"error": "Token is missing or invalid"}), 401

            token = auth_header.split()[1]

            if not token:
                return jsonify({"error": "Token is missing"}), 401

            decoded_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

            return f(decoded_data, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.exceptions.DecodeError:
            return jsonify({"error": "Not enough segments provided in token"})

        except Exception as e:
            return jsonify({"error": str(e)})

    return decorated_function


def currunt_user_data():
    try:
        token = request.headers.get("Authorization").split()[1]
        data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401

    except jwt.exceptions.DecodeError:
        return jsonify({"error": "Not enough segments provided in token"})

    except Exception:
        return jsonify({"error": "Internal server error from decorator"})
