import os
import random
from hashlib import sha256

from flask import jsonify, request

from src.common_crud.crud import CRUD
from src.database import db
from src.models.user import EmailOTP, User
from src.serializers.user_serializer import user_serializer
from src.utils.create_jwt import create_access_token, create_token_password
from src.utils.required_jwt_token import (
    currunt_user_data,
    login_required,
    token_required,
)
from src.utils.send_email import send_otp_by_email

user_crud = CRUD(User)

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


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

        check_email_exists = (
            db.session.query(User)
            .filter_by(is_deleted=False, email=user_details["email"])
            .first()
        )

        if check_email_exists:
            return jsonify({"error": "Email already exist"})

        # hash password
        password = hash_password(user_details.get("password"))

        # update password in dict
        user_details["password"] = password
        otp = random.randint(111111, 999999)

        user = User(**user_details)
        user.otp = otp
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        email_otp = EmailOTP(userid=user.id, email=user.email, otp=otp)
        db.session.add(email_otp)
        db.session.commit()
        db.session.refresh(email_otp)

        send_otp_by_email(user_details["email"], otp)
        return jsonify({"id": user.id, "message": "OTP Send To Your Mail successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


def varify_otp():
    data = request.json
    otp = data["otp"]
    email = data["email"]

    user_exist = db.session.query(User).filter(User.email == email).first()
    if not user_exist:
        return jsonify({"error": "Invalid User"})

    varify_user_otp = (
        db.session.query(EmailOTP)
        .filter(EmailOTP.email == email, EmailOTP.otp == otp)
        .first()
    )

    if not varify_user_otp:
        return jsonify({"error": "Invalid OTP"})

    user_exist.is_varify = True
    db.session.delete(varify_user_otp)
    db.session.commit()
    db.session.refresh(user_exist)

    # not execute or not working
    if not user_exist.is_varify:
        return jsonify({"message": "user varified"})

    token = create_token_password({"email": user_exist.email})
    return jsonify({"Token": token, "message": "user varified"})


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
        .filter_by(
            email=user_credential.get("email"),
            password=password,
            is_deleted=False,
        )
        .first()
    )

    if not user:
        return jsonify({"error": "Invalid email or password"})

    user_dict = {"id": user.id, "email": user.email}
    access_token = create_access_token(user_dict)

    return jsonify({"message": "Login successful", "token": access_token})


@token_required
def get_user_by_id(decoded_data):
    user_id = decoded_data.get("id")
    if not user_id:
        return jsonify({"error": "User not found"})
    return user_crud.get_by_id(user_id, user_serializer)


@login_required
def all_users():
    return user_crud.list_all()


@token_required
def update_user_details(decoded_data):
    user_id = decoded_data.get("id")
    user_details = request.json
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
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

    return {"user": user_serializer(user), "message": "User updated"}


@token_required
def change_user_password(decoded_data):
    user_id = decoded_data.get("id")
    user_details = request.json
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
    if "password" in user_details:
        # hash password
        password = hash_password(user_details.get("password"))
        user.password = password
    db.session.commit()
    db.session.refresh(user)
    return {"message": "Password updated"}


@token_required
def delete_user(decoded_data):
    user_id = decoded_data.get("id")
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
    user.is_deleted = True
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"message": "User Deleted"})


def forgot_password():
    data = request.json
    if not all(data.values()):
        return jsonify({"error": "email must be provided"})

    user_email = data["email"]

    user = (
        db.session.query(User)
        .filter_by(email=user_email, is_deleted=False, is_varify=True)
        .first()
    )
    if not user:
        return jsonify(
            {
                "error": """Forgot password is only available for registered users.
                            Please register first."""
            }
        )

    otp = random.randint(111111, 999999)

    email_otp_instance = EmailOTP(userid=user.id, email=user.email, otp=otp)
    db.session.add(email_otp_instance)
    db.session.commit()
    db.session.refresh(email_otp_instance)
    send_otp_by_email(user_email, otp)
    return jsonify({"message": "OTP Send To Your Mail successfully"})


def update_user_password():
    data = currunt_user_data()
    email = data["email"]
    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        return jsonify({"error": "Invalid Email"})
    data = request.json
    password = data["password"]
    password = hash_password(password)
    user.password = password
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"message": "Password is updated. login with new password"})


@token_required
def update_password_logic(decoded_data):
    email = decoded_data.get("email")

    # Retrieve the user from the database
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Extract and hash the new password from the JSON request
    request_data = request.get_json()
    password = request_data.get("password")
    if not password:
        return jsonify({"error": "Password is missing"}), 400

    # Hash the new password and update it in the database
    hashed_password = hash_password(password)
    user.password = hashed_password

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "Password is updated. Log in with your new password"})
