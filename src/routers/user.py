from flask import Blueprint

from src.views.user import (
    all_users,
    change_user_password,
    create_user,
    delete_user,
    forgot_password,
    get_user_by_id,
    login_user,
    update_user_details,
    update_user_password,
    varify_otp,
)

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    return create_user()


@user_bp.route("/login", methods=["POST"])
def login():
    return login_user()


@user_bp.route("/<userid>", methods=["GET"])
def get_user(userid):
    return get_user_by_id(userid)


@user_bp.route("/getall", methods=["GET"])
def get_all_users():
    return all_users()


@user_bp.route("<userid>", methods=["PATCH"])
def update_user(userid):
    return update_user_details(userid)


@user_bp.route("<userid>/password", methods=["PUT"])
def change_password(userid):
    return change_user_password(userid)


@user_bp.route("<userid>", methods=["DELETE"])
def delete(userid):
    return delete_user(userid)


@user_bp.route("otp", methods=["POST"])
def varify():
    return varify_otp()


@user_bp.route("/forgot_password", methods=["POST"])
def forgot():
    return forgot_password()


@user_bp.route("/update_password", methods=["POST"])
def update_password():
    return update_user_password()
