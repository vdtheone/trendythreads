import random
from hashlib import sha256

from flask import jsonify, request

from src.database import db
from src.models.user import EmailOTP, User
from src.utils.create_jwt import create_access_token
from src.utils.required_jwt_token import login_required
from src.utils.send_email import send_otp_by_email
from src.utils.user_serializer import user_serializer


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


@login_required
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


@login_required
def change_user_password(userid):
    user_details = request.json
    user = db.session.query(User).get(userid)
    if "password" in user_details:
        # hash password
        password = hash_password(user_details.get("password"))
        user.password = password
    db.session.commit()
    db.session.refresh(user)
    return {"message": "Password updated"}


@login_required
def delete_user(userid):
    user = db.session.query(User).get(userid)
    if not user:
        return jsonify({"error": "User not found"})
    user.is_deleted = True
    db.session.commit()
    db.session.refresh(user)
    return jsonify({"message": "User Deleted"})


def varify_otp(userid):
    data = request.json
    otp = data["otp"]

    varify_user_otp = (
        db.session.query(EmailOTP)
        .filter(EmailOTP.userid == userid, EmailOTP.otp == otp)
        .first()
    )

    if not varify_user_otp:
        return jsonify({"error": "Invalid OTP"})

    user = db.session.query(User).get(userid)

    user.is_varify = True

    db.session.delete(varify_user_otp)
    db.session.commit()
    db.session.refresh(user)

    return jsonify({"message": "user varified"})


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
    return jsonify({"id": user.id, "message": "OTP Send To Your Mail successfully"})
