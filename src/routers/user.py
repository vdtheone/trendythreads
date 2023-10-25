from flask import Blueprint

from src.views.user import (
    all_users,
    create_user,
    get_user_by_id,
    login_user,
    update_password,
    update_user_details,
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


@user_bp.route('<userid>/password', methods=['PUT'])
def change_password(userid):
    return update_password(userid)
