from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from src.database import db
from src.routers.cart import cart_bp
from src.routers.category import category_bp
from src.routers.order import order_bp
from src.routers.product import product_bp
from src.routers.user import configure_user_blueprint, user_bp


def create_app():
    app = Flask(__name__)

    # Setting up Flask-Limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    # Configuring the user blueprint (avoiding circular import)
    configure_user_blueprint(limiter)

    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(product_bp, url_prefix="/api/product")
    app.register_blueprint(category_bp, url_prefix="/api/category")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(order_bp, url_prefix="/api/order")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
