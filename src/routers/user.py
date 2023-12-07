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


def configure_user_blueprint(limiter):  # To avoid circular impport
    @user_bp.route("/varify_otp", methods=["POST"])
    @limiter.limit(
        "5 per minute"
    )  # Example rate limit: 5 attempts(requests) per minute
    def varify():
        return varify_otp()


@user_bp.route("/login", methods=["POST"])
def login():
    return login_user()


@user_bp.route("/profile", methods=["GET"])
def get_user():
    return get_user_by_id()


@user_bp.route("/getall", methods=["GET"])
def get_all_users():
    return all_users()


@user_bp.route("/update_profile", methods=["PATCH"])
def update_user():
    return update_user_details()


@user_bp.route("change_password", methods=["PUT"])
def change_password():
    return change_user_password()


@user_bp.route("/delete_account", methods=["DELETE"])
def delete():
    return delete_user()


@user_bp.route("/forgot_password", methods=["POST"])
def forgot():
    return forgot_password()


@user_bp.route("/update_password", methods=["POST"])
def update_password():
    return update_user_password()


# @user_bp.route('/update_password', methods=['POST'])
# def update_password():
#     return update_password_logic()
