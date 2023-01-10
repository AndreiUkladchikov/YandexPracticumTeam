# flask_app/app.py
import http
import os
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from flask_pydantic import validate

from config import settings
from db import db, init_db
from db_models import User
from forms import LoginForm

# def create_app():
#     app = Flask(__name__)
#     init_db(app)
#     app.app_context().push()
#     db.create_all()
#
#     SECRET_KEY = os.urandom(32)
#     app.config["SECRET_KEY"] = SECRET_KEY
#
#     app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
#     jwt = JWTManager(app)
#
#     return app


app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=settings.access_token_expires_in_hours
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    days=settings.refresh_token_expires_in_days
)

jwt = JWTManager(app)

init_db(app)
app.app_context().push()
db.create_all()


@app.route("/api/v1/auth/login", methods=["POST"])
@validate()
def check_login_password(body: LoginForm):
    user = User.query.filter_by(email=body.email).one_or_none()

    if not (user and user.check_password(body.password)):
        return jsonify({"msg": "Wrong email or password"}), http.HTTPStatus.UNAUTHORIZED

    # TODO Add additional_claims with role (https://flask-jwt-extended.readthedocs.io/en/stable/add_custom_data_claims/)

    additional_claims = {"role": "subscriber"}

    access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.email, additional_claims=additional_claims)

    user.refresh_token = refresh_token

    user.save_to_db()

    # TODO Put to DB (table: user_access): location, time
    return (
        jsonify(msg="Success authorization!", access_token=access_token, refresh_token=refresh_token),

        http.HTTPStatus.OK,
    )


@app.route("/api/v1/auth/registration", methods=["POST"])
@validate()
def registration(body: LoginForm):
    user = User(email=body.email)
    user.set_password(body.password)

    if User.query.filter_by(email=body.email).one_or_none():
        return (
            jsonify({"msg": "The email is already registered"}),
            http.HTTPStatus.UNAUTHORIZED,
        )

    user.save_to_db()

    return jsonify({"msg": "Thank you for registration!"}), http.HTTPStatus.OK


@app.route("/api/v1/auth/refresh-tokens", methods=["POST"])
@jwt_required(refresh=True)
def refresh_tokens():
    head = request.headers
    refresh = head.get('Authorization').split(" ")[-1]

    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).one_or_none()

    if refresh != user.refresh_token:
        user.refresh_token = None
        user.save_to_db()
        return (
            jsonify({"msg": "The token has not been confirmed. Go through authorization"}),
            http.HTTPStatus.UNAUTHORIZED,
        )

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    return jsonify(access_token=access_token, refresh_token=refresh_token)


# Test route
@app.route("/api/v1/auth/check", methods=["POST", "GET"])
@jwt_required()
def check():
    current_user = get_jwt_identity()
    return jsonify(msg="My congratulations", logged_in_as=current_user)


@app.route("/api/v1/auth/logout", methods=["POST", "GET"])
@jwt_required()
def logout():
    # TODO put access token to black list (Redis), delete refresh token from DB
    current_user = get_jwt_identity()
    return jsonify(msg=f"Logout from {current_user}"), http.HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
