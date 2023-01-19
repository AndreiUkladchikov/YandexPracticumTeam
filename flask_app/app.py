import os
from datetime import datetime, timedelta
from http import HTTPStatus

import redis
import requests
from flask import Flask, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt,
                                get_jwt_identity, jwt_required)
from flask_pydantic import validate
from loguru import logger

import constants
import messages
from clients import postgres_client
from config import settings
from db import db, init_db
from db_models import Role, User, UserAccessHistory, UserRole
from forms import LoginForm, PasswordResetForm
from messages import (HistoryResponseForm, ResponseForm,
                      ResponseFormWithTokens, SingleAccessRecord)
from services import (AccessHistoryService, RoleService, UserRoleService,
                      UserService)

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

user_service = UserService(postgres_client)
role_service = RoleService(postgres_client)
access_history_service = AccessHistoryService(postgres_client)
user_role_service = UserRoleService(postgres_client)


@app.route(f"{settings.base_api_url}/login", methods=["POST"])
@validate()
def check_login_password(body: LoginForm):
    user = user_service.get({"email": body.email})

    if not (user and user.check_password(body.password)):
        return ResponseForm(msg=messages.wrong_credits), HTTPStatus.UNAUTHORIZED

    additional_claims = {"role": "subscriber"}

    access_token = create_access_token(
        identity=user.email, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=user.email, additional_claims=additional_claims
    )

    user.refresh_token = refresh_token

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    user_service.insert(user)

    return ResponseFormWithTokens(
        msg=messages.success_login,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@app.route(f"{settings.base_api_url}/registration", methods=["POST"])
@validate()
def registration(body: LoginForm):

    if user_service.get({"email": body.email}):
        return ResponseForm(msg=messages.already_registered), HTTPStatus.UNAUTHORIZED

    user = User(email=body.email)
    user.set_password(body.password)
    user_service.insert(user)

    user = user_service.get({"email": body.email})

    role = role_service.get({"name": "subscriber"})

    user_role = UserRole(user_id=user.id, role_id=role.id)
    user_role_service.insert(user_role)

    return ResponseForm(msg=messages.success_registration)


@app.route(f"{settings.base_api_url}/refresh-tokens", methods=["POST"])
@validate()
@jwt_required(refresh=True)
def refresh_tokens():
    refresh = request.headers.get("Authorization").split(" ")[-1]

    current_user = get_jwt_identity()

    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    if refresh != user.refresh_token:
        user.refresh_token = None
        user_service.insert(user)
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    access_token = create_access_token(identity=current_user)
    refresh_token = create_refresh_token(identity=current_user)

    user.refresh_token = refresh_token
    user_service.insert(user)

    return ResponseFormWithTokens(
        msg=messages.success_refresh_tokens,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@app.route(f"{settings.base_api_url}/logout", methods=["POST", "GET"])
@validate()
@jwt_required()
def logout():
    current_user = get_jwt_identity()

    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    user.refresh_token = None
    user_service.insert(user)

    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(
        jti, "", ex=timedelta(hours=settings.access_token_expires_in_hours)
    )
    return ResponseForm(msg=messages.logout(current_user))


@app.route(f"{settings.base_api_url}/change-credits", methods=["POST"])
@validate()
@jwt_required()
def change_credits(body: PasswordResetForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not (user and user.check_password(body.previous_password)):
        return ResponseForm(msg=messages.wrong_credits), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    user.set_password(body.password)
    user.refresh_token = None
    user_service.insert(user)

    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(
        jti, "", ex=timedelta(hours=settings.access_token_expires_in_hours)
    )

    return ResponseForm(msg=messages.success_change_credits)


@app.route(f"{settings.base_api_url}/login-history", methods=["GET"])
@validate()
@jwt_required()
def get_login_history():
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    result = (
        db.session.query(
            User.email,
            UserAccessHistory.location,
            UserAccessHistory.device,
            UserAccessHistory.time,
        )
        .join(UserAccessHistory, User.id == UserAccessHistory.user_id)
        .filter(User.email == current_user)
        .all()
    )

    history = [SingleAccessRecord(**dict(s)) for s in result]
    return HistoryResponseForm(msg=messages.history_response, records=history)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@validate()
@jwt_required()
def catch_all(path):
    current_user = get_jwt_identity()

    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    result = (
        db.session.query(Role.permissions)
        .join(UserRole, Role.id == UserRole.role_id)
        .join(User, User.id == UserRole.user_id)
        .filter(User.email == current_user)
        .one_or_none()
    )

    if path in result["permissions"]:
        url = f"http://{settings.backend_host}:{settings.backend_port}/" + path
        req = requests.models.PreparedRequest()
        req.prepare_url(url, request.args.to_dict())
        return requests.get(req.url).json()
    else:
        return ResponseForm(msg=messages.not_allowed_resource), HTTPStatus.FORBIDDEN


def create_test_roles():
    try:
        role_service.insert(constants.ROLE_USER)
        role_service.insert(constants.ROLE_SUBSCRIBER)
        role_service.insert(constants.ROLE_ADMIN)
        role_service.insert(constants.ROLE_OWNER)
    except Exception:
        logger.info("Roles have been already created")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    postgres_client.create_all_tables()
    create_test_roles()
    app.run(host=settings.auth_server_host, port=settings.auth_server_port, debug=True)
