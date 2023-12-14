from datetime import date, datetime, timedelta
from io import BytesIO

from flask import Response, jsonify, request
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.database import db
from src.models.inventory import Inventory
from src.models.order import Invoice, Order, OrderItem
from src.models.product import Product
from src.serializers.order_serializer import order_serialzer
from src.utils.required_jwt_token import token_required


@token_required
def add_new_order(decoded_data):
    try:
        user_id = decoded_data.get("id")
        order_data = request.json
        for key, value in order_data.items():
            if value == "" or value is None:
                return jsonify({"error": f"The key '{key}' has no value."})
        product = (
            db.session.query(Product)
            .filter(Product.id == order_data["product_id"])
            .first()
        )

        # get available quantity
        available_quantity = (
            db.session.query(Inventory)
            .filter(Inventory.product_id == order_data["product_id"])
            .first()
            .stock_quantity
        )
        # check available quantity
        if not available_quantity >= order_data["quantity"]:
            return jsonify(
                {
                    "messages": "Out of stock",
                    "product": [{"id": product.id, "name": product.name}],
                }
            )

        total_amount = product.price * order_data["quantity"]

        new_order = Order(user_id=user_id)
        db.session.add(new_order)
        db.session.commit()
        db.session.refresh(new_order)

        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=order_data["product_id"],
            quantity=order_data["quantity"],
            total_amount=total_amount,
        )

        db.session.add(new_order_item)
        db.session.commit()
        db.session.refresh(new_order_item)

        # update inventory(stock)
        update_inventory = (
            db.session.query(Inventory)
            .filter(Inventory.product_id == new_order_item.product_id)
            .first()
        )
        update_inventory.stock_quantity -= new_order_item.quantity
        db.session.commit()
        db.session.refresh(new_order)
        return order_serialzer(new_order)

    except Exception as e:
        db.session.rollback()
        return {"Error": str(e)}
    finally:
        db.session.close()


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

    user_products = (
        db.session.query(OrderItem)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.user_id == user_id)
        .all()
    )

    total_order_amount = 0
    for product in user_products:
        total_order_amount += product.total_amount

    all_orders_data = [order.serialize() for order in orders]
    return jsonify(
        {
            "message": all_orders_data,
            "count": all_orders.count(),
            "Total_amount": total_order_amount,
        }
    )


def details_of_order(order_id):
    order = db.session.query(Order).get(order_id)
    if not order:
        return jsonify({"error": "Order not found"})
    return order.serialize()


def delete_order(order_id):
    order = db.session.query(Order).get(order_id)
    if not order:
        return jsonify({"error": "Order not found"})

    db.session.delete(order)
    db.session.commit()
    return jsonify({"messageg": "Order Deleted"})


# # this function update status of order. for now this functionality is not working.
# def order_status_update(order_id):
#     request_data = request.json
#     new_status = request_data["status"]
#     order = db.session.query(Order).get(order_id)
#     if not order:
#         return jsonify({"error": "order not found"})
#     if new_status not in [status.value for status in OrderStatus]:
#         return jsonify({"message": "Invalid status value"}), 400

#     order.status = OrderStatus(new_status)
#     db.session.commit()
#     db.session.refresh(order)
#     return jsonify({"message": "Order status updated successfully"})


def generate_invoice_of_order(order_id):
    order = db.session.query(Order).get(order_id)
    order_json = order.serialize()
    return jsonify({"order": order_json})


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
    order = db.session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        return jsonify({"error": "order not found"})
    insert_invoice_data(order_id)
    return order


def generate_invoice_pdf(order_obj):
    def draw_field(p, label, value, x, y, title_style):
        p.setFont(title_style, 12)
        p.drawString(x, y, f"{label}")

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    title_style = "Helvetica-Bold"
    field_style = "Helvetica"

    p.setFont(title_style, 18)
    p.drawCentredString(300, 750, "Invoice")

    y = 700
    x_start = 50
    row_height = 20

    # Header
    header_fields = ["Product Name", "Price Per Unit", "Quantity", "Total Amount"]
    x_positions = [50, 200, 350, 500]
    row_height = 20

    for index, field in enumerate(header_fields):
        draw_field(p, field, "", x_positions[index], y, title_style)

    y -= row_height

    product_data = (
        db.session.query(OrderItem).filter(OrderItem.order_id == order_obj.id).all()
    )

    grand_total = 0
    for index, prod in enumerate(product_data):
        draw_field(
            p, prod.product.name, "", x_start, y - (row_height * index), field_style
        )
        draw_field(
            p,
            prod.product.price,
            "",
            x_start + 150,
            y - (row_height * index),
            field_style,
        )
        draw_field(
            p, prod.quantity, "", x_start + 300, y - (row_height * index), field_style
        )
        draw_field(
            p,
            float(prod.total_amount),
            "",
            x_start + 450,
            y - (row_height * index),
            field_style,
        )

        grand_total += float(prod.total_amount)

    # Grand Total
    y -= row_height * (len(product_data) + 1)
    draw_field(p, "Grand Total = ", "", x_start, y, title_style)
    draw_field(p, grand_total, "", x_start + 80, y, title_style)

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


@token_required
def add_multiple_order(decoded_data):
    order_details = request.json
    user_id = decoded_data.get("id")
    new_order = Order(user_id=user_id)
    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)
    for order in order_details:
        for key, value in order.items():
            if value == "" or value is None:
                return jsonify({"error": f"The key '{key}' has no value."})

        product = (
            db.session.query(Product).filter(Product.id == order["product_id"]).first()
        )

        # get available quantity
        available_quantity = (
            db.session.query(Inventory)
            .filter(Inventory.product_id == order["product_id"])
            .first()
            .stock_quantity
        )
        # check available quantity
        if not available_quantity >= order["quantity"]:
            return jsonify(
                {
                    "messages": "Out of stock",
                    "product": [{"id": product.id, "name": product.name}],
                }
            )

        total_amount = product.price * order["quantity"]

        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=order["product_id"],
            quantity=order["quantity"],
            total_amount=total_amount,
        )

        db.session.add(new_order_item)
        db.session.commit()
        db.session.refresh(new_order_item)

        # update inventory(stock)
        update_inventory = (
            db.session.query(Inventory)
            .filter(Inventory.product_id == new_order_item.product_id)
            .first()
        )
        update_inventory.stock_quantity -= new_order_item.quantity
        db.session.commit()
        db.session.refresh(update_inventory)
    return order_serialzer(new_order)
