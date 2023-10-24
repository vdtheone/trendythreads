from hashlib import sha256
from sqlalchemy.exc import IntegrityError
from src.models.user import User
from flask import jsonify, request

from src.utils.create_jwt import create_access_token
from src.utils.user_serializer import user_serializer
from src.utils.required_jwt_token import login_required
from src.database import db


def hash_password(password: str):
    hash_obj = sha256()
    hash_obj.update(password.encode("utf-8"))
    hashed_password = hash_obj.hexdigest()
    return hashed_password


def create_user():
    try:
        # get all details from request
        user_details = request.json

        # check if any value is none
        for key, value in user_details.items():
            if value == "" or value is None:
                return jsonify({"error": f"The key '{key}' has no value."})

        # hash password
        password = hash_password(user_details.get("password"))

        # update password in dict
        user_details["password"] = password

        user = User(**user_details)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return jsonify({"message": "User created successfully"})
    except IntegrityError as e:
        return jsonify({"error": f"Email already exist"})
    # except Exception as e:
    #     return jsonify({"error": str(e)})


def login_user():
    user_credential = request.json

    # check if any value is none
    for key, value in user_credential.items():
        if value == "" or value is None:
            return jsonify({"error": f"The key '{key}' has no value."})

    # first hash password and after compare with database
    password = hash_password(user_credential.get("password"))

    # check credential of user in database
    user = (
        db.session.query(User)
        .filter(
            User.email == user_credential.get("email"),
            User.password == password,
        )
        .first()
    )

    if not user:
        return jsonify({"error": "Invalid email or password"})

    user_dict = {"id": user.id, "email": user.email}
    access_token = create_access_token(user_dict)

    return jsonify({"message": "Login successful", "token": access_token})


def get_user_by_id(userid):
    user = db.session.query(User).get(userid)
    if not user:
        return jsonify({"error": "User not found"})
    return user_serializer(user)


@login_required
def all_users():
    users = db.session.query(User).all()
    if not users:
        return jsonify({"error": "User not found"})
    user_list = []

    for user in users:
        user_dict = user_serializer(user)
        user_list.append(user_dict.json)
    return user_list


@login_required
def update_user_details(userid):
    user_details = request.json
    user = db.session.query(User).get(userid)
    if "first_name" in user_details:
        user.first_name = user_details["first_name"]
    if "last_name" in user_details:
        user.last_name = user_details["last_name"]
    if "email" in user_details:
        user.email = user_details["email"]
    if "mobile_no" in user_details:
        user.mobile_no = user_details["mobile_no"]

    db.session.commit()
    db.session.refresh(user)

    return {"user": user_serializer(user).json, "message": "User updated"}


def update_password(userid):
    user_details = request.json
    user = db.session.query(User).get(userid)
    if "password" in user_details:
        # hash password
        password = hash_password(user_details.get("password"))
        user.password = password
    db.session.commit()
    db.session.refresh(user)
    return {"message":"Password updated"}
    
