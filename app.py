from flask import Flask

from config import Config
from src.database import db
from src.routers.user import user_bp


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    app.register_blueprint(user_bp, url_prefix="/api/users")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
