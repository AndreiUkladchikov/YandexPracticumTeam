# flask_app/app.py
import http
import os
import uuid
from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_pydantic import validate

from config import settings
from db_models import User
from flask_app.clients import postgres_client
from forms import LoginForm
from services import UserService

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    seconds=settings.access_token_expires_in_seconds
)

jwt = JWTManager(app)
app.app_context().push()
user_service = UserService(postgres_client)


@app.route(f"{settings.base_api_url}/login", methods=["POST"])
@validate()
def check_login_password(body: LoginForm):
    user = user_service.get({"email": body.email})

    if not (user and user.check_password(body.password)):
        return jsonify({"msg": "Wrong email or password"}), http.HTTPStatus.UNAUTHORIZED

    # TODO Add additional_claims with role (https://flask-jwt-extended.readthedocs.io/en/stable/add_custom_data_claims/)
    additional_claims = {"role": "subscriber", "foo": "bar"}
    # TODO
    access_token = create_access_token(identity=user.email)

    print("Success authorization!")

    # TODO Put to DB (table: user_access): location, refresh_token, time
    # TODO Generate refresh_token, put it to DB
    return (
        jsonify(msg="Success authorization!", access_token=access_token),
        http.HTTPStatus.OK,
    )


@app.route(f"{settings.base_api_url}/registration", methods=["POST"])
@validate()
def registration(body: LoginForm):
    if user_service.get({"email": body.email}):
        return (
            jsonify({"msg": "The email is already registered"}),
            http.HTTPStatus.UNAUTHORIZED,
        )

    user = User(email=body.email)
    user.set_password(body.password)
    user_service.insert(user)

    return jsonify({"msg": "Thank you for registration!"}), http.HTTPStatus.OK


@app.route(f"{settings.base_api_url}/refresh-tokens", methods=["POST"])
def refresh_token():
    pass


# Test route
@app.route(f"{settings.base_api_url}/check", methods=["POST", "GET"])
@jwt_required()
def check():
    current_user = get_jwt_identity()
    return jsonify(msg="My congratulations", logged_in_as=current_user)


@app.route(f"{settings.base_api_url}/logout", methods=["POST", "GET"])
@jwt_required()
def logout():
    # TODO put access token to black list (Redis), delete refresh token from DB
    current_user = get_jwt_identity()
    return jsonify(msg=f"Logout from {current_user}"), http.HTTPStatus.OK


if __name__ == "__main__":
    postgres_client.create_all_tables()
    app.run(debug=True)
