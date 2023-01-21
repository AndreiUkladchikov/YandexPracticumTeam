import os
from datetime import datetime, timedelta
from http import HTTPStatus

import redis
import requests
from flask import Flask, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt,
                                get_jwt_identity, jwt_required)
from loguru import logger
from spectree import Response, SpecTree

import constants
import messages
from clients import postgres_client
from config import settings
from db import init_db
from db_models import Role, User, UserAccessHistory, UserRole
from forms import LoginForm, PasswordResetForm, RoleForm, UserRoleForm
from messages import (HistoryResponseForm, ResponseForm,
                      ResponseFormWithTokens, SingleAccessRecord,
                      RoleRecord, RolesResponseForm)
from services import (AccessHistoryService, CustomService, UserRoleService)

app = Flask(__name__)
spec = SpecTree("flask", annotations=True)
spec.register(app)

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

user_service = CustomService(client=postgres_client, model=User)
role_service = CustomService(client=postgres_client, model=Role)
access_history_service = AccessHistoryService(postgres_client)
user_role_service = UserRoleService(postgres_client)


def check_path(permission: list[str], url_path: str) -> bool:
    for p in permission:
        if url_path.startswith(p):
            return True
    return False


@app.route(f"{settings.base_api_url}/login", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseFormWithTokens, HTTP_401=ResponseForm), tags=["api"]
)
def check_login_password(json: LoginForm):
    user = user_service.get({"email": json.email})

    if not (user and user.check_password(json.password)):
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
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
def registration(json: LoginForm):
    if user_service.get({"email": json.email}):
        return ResponseForm(msg=messages.already_registered), HTTPStatus.UNAUTHORIZED

    user = User(email=json.email)
    user.set_password(json.password)
    user_service.insert(user)

    user = user_service.get({"email": json.email})

    role = role_service.get({"name": "subscriber"})

    user_role = UserRole(user_id=user.id, role_id=role.id)
    user_role_service.insert(user_role)

    return ResponseForm(msg=messages.success_registration)


@app.route(f"{settings.base_api_url}/refresh-tokens", methods=["GET"])
@spec.validate(
    resp=Response(HTTP_200=ResponseFormWithTokens, HTTP_401=ResponseForm), tags=["api"]
)
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


@app.route(f"{settings.base_api_url}/logout", methods=["GET"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
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
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
@jwt_required()
def change_credits(json: PasswordResetForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not (user and user.check_password(json.previous_password)):
        return ResponseForm(msg=messages.wrong_credits), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    user.set_password(json.password)
    user.refresh_token = None
    user_service.insert(user)

    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(
        jti, "", ex=timedelta(hours=settings.access_token_expires_in_hours)
    )

    return ResponseForm(msg=messages.success_change_credits)


@app.route(f"{settings.base_api_url}/login-history", methods=["GET"])
@spec.validate(
    resp=Response(HTTP_200=HistoryResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
@jwt_required()
def get_login_history():
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    result = access_history_service.get_detailed_info_about(current_user)

    history = [SingleAccessRecord(**dict(s)) for s in result]
    return HistoryResponseForm(msg=messages.history_response, records=history)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm, HTTP_403=ResponseForm, HTTP_500=ResponseForm),
    tags=["api"],
)
@jwt_required(optional=True)
def catch_all(path):
    current_user = get_jwt_identity()

    if not current_user:
        result = {"permissions": constants.ROLE_UNAUTHORIZED_USER.permissions}
    else:
        user: User = user_service.get({"email": current_user})

        if not user:
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

        result = get_permissions(current_user)

    if check_path(result["permissions"], path):
        url = f"http://{settings.backend_host}:{settings.backend_port}/" + path
        req = requests.models.PreparedRequest()
        req.prepare_url(url, request.args.to_dict())
        return ResponseForm(msg=messages.successful_response, result=requests.get(req.url).json())
    else:
        print("bad")
        return ResponseForm(msg=messages.not_allowed_resource), HTTPStatus.FORBIDDEN


# Roles CRUD:

# Update or Create
@app.route(f"{settings.base_api_url}/update-role", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
@jwt_required()
def update_role(body: RoleForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        print("unathorized")
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        print(user.id)
        result = user_role_service.get_permissions_of(user)
        if check_path(result["permissions"], "update-role"):
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    if body.id is None:
        role_service.insert(
            Role(
                name=body.name,
                permissions=body.permissions,
                access_level=body.access_level
            )
        )
        msg = messages.success_create_role
    else:
        role = role_service.get({"id": body.id})
        role_service.update(role, body.__dict__)
        msg = messages.success_update_role

    return ResponseForm(msg=msg)


# Delete
@app.route(f"{settings.base_api_url}/delete-role", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
@jwt_required()
def delete_role(body: RoleForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if check_path(result["permissions"], "delete-role"):
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    role = role_service.get({"id": body.id})
    role_service.delete(role)

    return ResponseForm(msg=messages.success_delete_role)


@app.route(f"{settings.base_api_url}/get-all-roles", methods=["GET"])
@spec.validate(
    resp=Response(HTTP_200=RolesResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
@jwt_required()
def get_all_roles():
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if check_path(result["permissions"], "get-all-roles"):
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    result = role_service.all()
    roles = [RoleRecord(**s.__dict__) for s in result]
    return RolesResponseForm(msg=messages.roles_response, records=roles)


@app.route(f"{settings.base_api_url}/update-user-role", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["api"]
)
@jwt_required()
def update_user_role(body: UserRoleForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if "update-role" not in result["permissions"]:
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    if body.id is None:
        role_service.insert(
            UserRole(
                user_id=body.user_id,
                role_id=body.role_id
            )
        )
    else:
        role = role_service.get({"id": body.id})
        role_service.update(role, body.__dict__)

    return ResponseForm(msg=messages.success_update_user_role)


def create_test_roles():
    try:
        role_service.insert(constants.ROLE_USER)
        role_service.insert(constants.ROLE_SUBSCRIBER)
        role_service.insert(constants.ROLE_ADMIN)
        role_service.insert(constants.ROLE_OWNER)
    except Exception:
        logger.info("Roles have been already created")


def create_test_admin():
    try:
        user_service.insert(constants.TEST_ADMIN)
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except Exception:
        logger.info("Admin has been already created")


def grant_test_admin_role():
    try:
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except Exception:
        logger.info("Admin already has access")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    postgres_client.create_all_tables()
    create_test_roles()
    create_test_admin()
    grant_test_admin_role()
    app.run(host=settings.auth_server_host, port=settings.auth_server_port, debug=True)
