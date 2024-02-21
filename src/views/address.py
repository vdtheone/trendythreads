from flask import g, jsonify, request

from src.common_crud.crud import CRUD
from src.database import db
from src.models.address import Address
from src.utils.required_jwt_token import login_required

address_crud = CRUD(Address)


@login_required
def add_address():
    address = request.json
    responce = address_crud.create(address)
    return responce


@login_required
def all_address():
    user_id = g.user
    addresses = db.session.query(Address).filter(Address.user_id == user_id).all()
    responce = [address.serialize() for address in addresses]
    return jsonify({"user_id": user_id, "Addresses": responce})


@login_required
def edit_address(address_id):
    address = request.json
    responce = address_crud.update(address_id, address)
    return responce


@login_required
def delete_address(address_id):
    return address_crud.delete(address_id)
