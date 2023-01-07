from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import settings

db = SQLAlchemy()


def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{settings.auth_db_username}:"
        f"{settings.auth_db_password}@{settings.auth_db_host}/{settings.auth_db_name}"
    )
    db.init_app(app)
