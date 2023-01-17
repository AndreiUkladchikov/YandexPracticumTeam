# flask_app/app.py
import http
import os
import redis
from datetime import timedelta, datetime, timezone

from loguru import logger
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask_pydantic import validate

import messages
from config import settings
from db import db, init_db
from db_models import User, UserAccessHistory, UserRole, Role
from forms import LoginForm, PasswordResetForm
from messages import SingleAccessRecord, HistoryResponseForm


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

jwt_redis_blocklist = redis.StrictRedis(
    host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True
)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = True
    try:
        token_in_redis = jwt_redis_blocklist.get(jti)
    except redis.exceptions.ConnectionError:
        logger.error("Redis is not available!")
    return token_in_redis is not None


init_db(app)
app.app_context().push()
db.create_all()


@app.route("/api/v1/auth/login", methods=["POST"])
@validate()
def check_login_password(body: LoginForm):
    user = User.query.filter_by(email=body.email).one_or_none()

    if not (user and user.check_password(body.password)):
        return jsonify(messages.wrong_credits), http.HTTPStatus.UNAUTHORIZED

    additional_claims = {"role": "subscriber"}

    access_token = create_access_token(
        identity=user.email, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=user.email, additional_claims=additional_claims
    )

    user.refresh_token = refresh_token

    access = UserAccessHistory(user_id=user.id, time=datetime.now())

    user.save_to_db()
    access.save_to_db()

    # TODO Put to DB (table: user_access): location, time
    return (
        jsonify(
            msg="Success authorization!",
            access_token=access_token,
            refresh_token=refresh_token,
        ),
        http.HTTPStatus.OK,
    )


@app.route("/api/v1/auth/registration", methods=["POST"])
@validate()
def registration(body: LoginForm):

    if User.query.filter_by(email=body.email).one_or_none():
        return (
            jsonify(messages.already_registered),
            http.HTTPStatus.UNAUTHORIZED,
        )

    user = User(email=body.email)
    user.set_password(body.password)

    user.save_to_db()

    return jsonify(messages.success_registration), http.HTTPStatus.OK


@app.route("/api/v1/auth/refresh-tokens", methods=["POST"])
@jwt_required(refresh=True)
def refresh_tokens():
    refresh = request.headers.get("Authorization").split(" ")[-1]

    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).one_or_none()

    if user is None:
        return jsonify(messages.bad_token), http.HTTPStatus.UNAUTHORIZED

    if refresh != user.refresh_token:
        user.refresh_token = None
        user.save_to_db()
        return (
            jsonify(messages.bad_token),
            http.HTTPStatus.UNAUTHORIZED,
        )

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    user.refresh_token = refresh_token
    user.save_to_db()

    return jsonify(access_token=access_token, refresh_token=refresh_token), http.HTTPStatus.OK


@app.route("/api/v1/auth/logout", methods=["POST", "GET"])
@jwt_required()
def logout():
    current_user = get_jwt_identity()

    user = User.query.filter_by(email=current_user).one_or_none()
    if user is None:
        return jsonify(messages.bad_token), http.HTTPStatus.UNAUTHORIZED

    user.refresh_token = None
    user.save_to_db()

    UserAccessHistory(user_id=user.id, time=datetime.now()).save_to_db()

    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(
        jti, "", ex=timedelta(hours=settings.access_token_expires_in_hours)
    )

    return jsonify(msg=f"Logout from {current_user}"), http.HTTPStatus.OK


@app.route("/api/v1/auth/change-credits", methods=["POST"])
@validate()
@jwt_required()
def change_credits(body: PasswordResetForm):
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).one_or_none()

    if not (user and user.check_password(body.previous_password)):
        return jsonify(messages.wrong_credits), http.HTTPStatus.UNAUTHORIZED

    user.set_password(body.password)
    user.refresh_token = None
    user.save_to_db()

    UserAccessHistory(user_id=user.id, time=datetime.now()).save_to_db()

    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(
        jti, "", ex=timedelta(hours=settings.access_token_expires_in_hours)
    )

    return jsonify(messages.success_change_credits), http.HTTPStatus.OK


@app.route("/api/v1/auth/login-history", methods=["GET"])
@validate()
@jwt_required()
def get_login_history():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).one_or_none()

    if not user:
        return jsonify(messages.bad_token), http.HTTPStatus.UNAUTHORIZED

    result = db.session.query(
        User.email, UserAccessHistory.location, UserAccessHistory.device, UserAccessHistory.time
    ).join(UserAccessHistory, User.id == UserAccessHistory.user_id).filter(User.email == current_user).all()

    history = [SingleAccessRecord(**dict(s)) for s in result]
    return HistoryResponseForm(msg=messages.history_response.get("msg"), records=history)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
# @jwt_required(optional=True)
def catch_all(path):
    # current_user = get_jwt_identity()
    current_user = "mikegot@mail.ru"

    user = User.query.filter_by(email=current_user).one_or_none()

    if not user:
        return jsonify(messages.bad_token), http.HTTPStatus.UNAUTHORIZED

    permissions = db.session.query(
        Role.permissions
    ).join(UserRole, Role.id == UserRole.role_id).join(User, User.id == UserRole.user_id).filter(User.email == current_user).one_or_none()

    print(type(permissions))
    print(dict(permissions))

    if path in permissions['permissions']:
        print("Welcome")
    else:
        return jsonify(messages.not_allowed_resource), http.HTTPStatus.FORBIDDEN

    return 'You want path: %s' % path


if __name__ == "__main__":
    app.run(debug=True)
