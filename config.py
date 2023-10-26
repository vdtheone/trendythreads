import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
