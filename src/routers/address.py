from flask import Blueprint

from src.views.address import add_address, all_address, delete_address, edit_address

address_bp = Blueprint("address", __name__)


@address_bp.route("/add-address", methods=['POST'])
def add_new_address():
    return add_address()


@address_bp.route("all-address", methods=['GET'])
def get_all_address():
    return all_address()


@address_bp.route("edit-address/<address_id>", methods=["PATCH"])
def update_address(address_id):
    return edit_address(address_id)


@address_bp.route("delete/<address_id>", methods=["DELETE"])
def remove_address(address_id):
    return delete_address(address_id)
