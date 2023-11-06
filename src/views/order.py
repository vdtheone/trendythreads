from datetime import date, datetime, timedelta
from io import BytesIO

from flask import Response, jsonify, request
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.database import db
from src.models.order import Order, OrderStatus
from src.utils.required_jwt_token import token_required


@token_required
def add_new_order(decoded_data):
    user_id = decoded_data.get("id")
    order_data = request.json
    for key, value in order_data.items():
        if value == "" or value is None:
            return jsonify({"error": f"The key '{key}' has no value."})
    new_order = Order(user_id=user_id, status=OrderStatus.ORDER_PLACED, **order_data)
    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)
    return {"message": "Order Placed Successfully"}


@token_required
def filter_order(decoded_data):
    user_id = decoded_data.get("id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date_obj + timedelta(days=1)

    if start_date is None or end_date is None:
        today = date.today()
        start_date = today
        end_date = today + timedelta(days=1)

    orders = (
        db.session.query(Order)
        .filter(
            Order.user_id == user_id, Order.created_at.between(start_date, end_date)
        )
        .all()
    )
    filtered_orders = [order.serialize() for order in orders]
    return jsonify({"message": filtered_orders, "count": len(filtered_orders)})


@token_required
def order_by_customer(decoded_data):
    user_id = decoded_data.get("id")
    orders = db.session.query(Order).filter(Order.user_id == user_id).all()
    all_orders = [order.serialize() for order in orders]
    return jsonify({"message": all_orders, "count": len(all_orders)})


def details_of_order(order_id):
    order = db.session.query(Order).get(order_id)
    if not order:
        return jsonify({"error": "Order not found"})


def delete_order(order_id):
    order = db.session.query(Order).get(order_id)
    if not order:
        return jsonify({"error": "Order not found"})

    db.session.delete(order)
    db.session.commit()
    return jsonify({"messageg": "Order Deleted"})


def order_status_update(order_id):
    request_data = request.json
    new_status = request_data["status"]
    order = db.session.query(Order).get(order_id)
    if not order:
        return jsonify({"error": "order not found"})
    if new_status not in [status.value for status in OrderStatus]:
        return jsonify({"message": "Invalid status value"}), 400

    order.status = OrderStatus(new_status)
    db.session.commit()
    db.session.refresh(order)
    return jsonify({"message": "Order status updated successfully"})


def generate_invoice_of_order(order_id):
    order = db.session.query(Order).get(order_id)
    order_json = order.serialize()
    return jsonify({"order": order_json})


def get_invoice_data(order_id):
    # Replace this with your logic to retrieve invoice data
    order = db.session.query(Order).get(order_id)
    if order is None:
        return None
    order_json = order.serialize()
    return order_json


def generate_invoice_pdf(order_data):
    # Create a BytesIO buffer to store the PDF data
    buffer = BytesIO()

    # Create a PDF canvas with letter size (8.5x11 inches)
    p = canvas.Canvas(buffer, pagesize=A4)

    # Define styles
    title_style = "Helvetica-Bold"
    field_style = "Helvetica"

    # Centered title
    p.setFont(title_style, 16)
    p.drawCentredString(300, 750, "Invoice")  # Centered title at (300, 750)

    # Set starting y-coordinate for fields
    y = 700

    # Iterate through fields and add them to the PDF
    fields = order_data
    for field, value in fields.items():
        p.setFont(field_style, 12)
        p.drawString(100, y, f"{field.replace('_', ' ').title()}:")
        p.setFont(field_style, 10)
        p.drawString(250, y, str(value))
        y -= 20  # Adjust the y-coordinate for the next field

    # Save the PDF content to the buffer
    p.save()

    # Reset the buffer position to the beginning
    buffer.seek(0)

    return buffer


def send_pdf_as_attachment(pdf_data):
    return Response(
        pdf_data.read(),
        headers={
            "Content-Type": "application/pdf",
            "Content-Disposition": "attachment; filename=invoice.pdf",
        },
    )
