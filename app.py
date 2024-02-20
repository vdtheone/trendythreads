from flask import Flask
from flask_cors import CORS

# Importing Flask-Limiter modules
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Importing your configurations and blueprints
from config import Config
from src.database import db
from src.routers.address import address_bp
from src.routers.cart import cart_bp
from src.routers.category import category_bp
from src.routers.inventory import inventory_bp
from src.routers.order import order_bp
from src.routers.product import product_bp
from src.routers.user import configure_user_blueprint, user_bp

# handle file uploads

UPLOAD_FOLDER = 'E:\\Internship\\Flask\\trendythreads\\src\\static\\uploads'


def create_app():
    app = Flask(__name__)

    # Setting up Flask-Limiter
    limiter = Limiter(
        app=app,  # Passing the Flask app instance
        key_func=get_remote_address,  # Function to get the remote IP address
        default_limits=["2000000 per day", "5000 per hour"],  # Default rate limits
        storage_uri="memory://",  # Using in-memory storage (for demonstration purposes)
    )

    # Enable CORS for all routes
    # CORS(app)  # This enables CORS for all origins.
    CORS(app, origins=["http://localhost:5173"])

    # Configuring the user blueprint (avoiding circular import)
    configure_user_blueprint(limiter)

    # Setting up app configurations
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['MAX_CONTENT_PATH'] = 1024

    db.init_app(app)

    # Registering all blueprints with their respective URL prefixes
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(product_bp, url_prefix="/api/product")
    app.register_blueprint(category_bp, url_prefix="/api/category")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(order_bp, url_prefix="/api/order")
    app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
    app.register_blueprint(address_bp, url_prefix="/api/address")

    return app


# Creating the app instance
app = create_app()

# Running the app only if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
