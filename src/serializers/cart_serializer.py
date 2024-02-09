from src.database import db
from src.models.product import Product


def cart_serializer(cart):
    product = db.session.query(Product).filter(Product.id == cart.product_id).first()

    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "product_id": cart.product_id,
        "quantity": cart.quantity,
        "name": product.name,
        "price": product.price,
        "brand": product.brand,
        "image": product.image,
    }
