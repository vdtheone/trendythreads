from datetime import date, datetime, timedelta
from io import BytesIO

from flask import Response, jsonify, request
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.database import db
from src.models.order import Invoice, Order, OrderStatus
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
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    user_id = decoded_data.get("id")
    offset = (page - 1) * limit
    all_orders = db.session.query(Order)
    orders = (
        all_orders.filter(Order.user_id == user_id).limit(limit).offset(offset).all()
    )
    all_orders_data = [order.serialize() for order in orders]
    return jsonify({"message": all_orders_data, "count": all_orders.count()})


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


# def generate_invoice_of_order(order_id):
#     order = db.session.query(Order).get(order_id)
#     order_json = order.serialize()
#     return jsonify({"order": order_json})


def insert_invoice_data(order_id):
    invoice_data = (
        db.session.query(Invoice).filter(Invoice.order_id == order_id).first()
    )
    if not invoice_data:
        data = {"order_id": order_id}
        invoice = Invoice(**data)
        db.session.add(invoice)
        db.session.commit()
        db.session.refresh(invoice)


def get_invoice_data(order_id):
    # Replace this with your logic to retrieve invoice data
    order = db.session.query(Order).get(order_id)
    if order is None:
        return jsonify({"error": "order not found"})
    insert_invoice_data(order_id)
    return order


def generate_invoice_pdf(order_obj):
    def draw_field(p, field, value, x, y):
        p.setFont(field_style, 18)
        p.drawString(x, y, f"{field.replace('_', ' ').title()}")
        p.setFont(field_style, 16)
        p.drawString(x + 150, y, " :   " + str(value))

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    title_style = "Helvetica-Bold"
    field_style = "Helvetica"

    p.setFont(title_style, 24)
    p.drawCentredString(300, 750, "Invoice")

    y = 700

    order_data = order_obj.serialize()

    invoice_obj = (
        db.session.query(Invoice).filter(Invoice.order_id == order_data["id"]).first()
    )

    # Fields to be displayed in the invoice with the desired order
    fields_to_display = {
        "Invoice Id": invoice_obj.id,
        "Name": f"{order_obj.user.first_name} {order_obj.user.last_name}",
        "Email": order_obj.user.email,
        "Created At": order_data["created_at"],
        "Quantity": order_data["quantity"],
        "Total Amount": order_data["total_amount"],
    }

    for field, value in fields_to_display.items():
        draw_field(p, field, value, 100, y)
        y -= 20

    p.save()
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
