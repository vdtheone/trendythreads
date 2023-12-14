from flask import Blueprint, jsonify

from src.views.order import (  # order_status_update,
    add_multiple_order,
    add_new_order,
    delete_order,
    details_of_order,
    filter_order,
    generate_invoice_pdf,
    get_invoice_data,
    insert_invoice_data,
    order_by_customer,
    send_pdf_as_attachment,
)

order_bp = Blueprint("order", __name__)


@order_bp.route("/new_order", methods=["POST"])
def new_order():
    return add_new_order()


@order_bp.route("/filter", methods=["GET"])
def filter():
    return filter_order()


@order_bp.route("/by_customer", methods=["GET"])
def by_customer():
    return order_by_customer()


@order_bp.route("/get_by_id/<order_id>", methods=["GET"])
def order_details(order_id):
    return details_of_order(order_id)


@order_bp.route("/order_delete/<order_id>", methods=["DELETE"])
def order_delete(order_id):
    return delete_order(order_id)


@order_bp.route("/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    return jsonify(
        {"Error": "for now this functionality is not working we will work on this."}
    )
    # return order_status_update(order_id)


# @order_bp.route("/<order_id>/invoice", methods=["GET"])
# def generate_invoice(order_id):
#     return generate_invoice_of_order(order_id)


@order_bp.route("/<order_id>/invoice", methods=["GET"])
def generate_invoice(order_id):
    order_obj = get_invoice_data(order_id)
    if order_obj is None:
        return jsonify({"error": "Order not found"})
    else:
        insert_invoice_data(order_obj.id)
        # Generate the PDF invoice
        pdf_data = generate_invoice_pdf(order_obj)

        # Serve the PDF as a downloadable attachment
        return send_pdf_as_attachment(pdf_data)


@order_bp.route("/multiple_order", methods=["POST"])
def new_multiple_order():
    return add_multiple_order()
