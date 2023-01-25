from datetime import datetime, timedelta
from http import HTTPStatus
from math import ceil

from flask import Blueprint, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from spectree import Response

import messages
from black_list import jwt_redis_blocklist
from config import settings
from db_models import User, UserAccessHistory, UserRole
from documentation import spec
from forms import LoginForm, PasswordResetForm
from limiter import limiter
from messages import (HistoryResponseForm, ResponseForm,
                      ResponseFormWithTokens, SingleAccessRecord)
from services import (access_history_service, role_service, user_role_service,
                      user_service)

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["POST"])
@limiter.limit(settings.rate_limit)
@spec.validate(
    resp=Response(HTTP_200=ResponseFormWithTokens, HTTP_401=ResponseForm), tags=["Auth"]
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


@auth_blueprint.route("/registration", methods=["POST"])
@limiter.limit(settings.rate_limit)
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["Auth"]
)
def registration(json: LoginForm):
    if user_service.get({"email": json.email}):
        return ResponseForm(msg=messages.already_registered), HTTPStatus.UNAUTHORIZED

    print(json.email)

    user = User(email=json.email)
    user.set_password(json.password)
    user_service.insert(user)

    user = user_service.get({"email": json.email})

    role = role_service.get({"name": "subscriber"})

    user_role = UserRole(user_id=user.id, role_id=role.id)
    user_role_service.insert(user_role)

    return ResponseForm(msg=messages.success_registration)


@auth_blueprint.route("/refresh-tokens", methods=["GET"])
@limiter.limit(settings.rate_limit)
@spec.validate(
    resp=Response(HTTP_200=ResponseFormWithTokens, HTTP_401=ResponseForm), tags=["Auth"]
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


@auth_blueprint.route(f"/logout", methods=["GET"])
@limiter.limit(settings.rate_limit)
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["Auth"]
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


@auth_blueprint.route("/change-credits", methods=["POST"])
@limiter.limit(settings.rate_limit)
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["Auth"]
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


@auth_blueprint.route("/login-history", methods=["GET"])
@limiter.limit(settings.rate_limit)
@spec.validate(
    resp=Response(HTTP_200=HistoryResponseForm, HTTP_401=ResponseForm), tags=["Auth"]
)
@jwt_required()
def get_login_history():
    args = request.args
    page_num = int(args.get("page_num", 1))
    page_size = int(args.get("page_size", 20))

    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    access_history_service.insert(
        UserAccessHistory(user_id=user.id, time=datetime.now())
    )

    result, total = access_history_service.get_detailed_info_about(
        user=user, page_size=page_size, page_num=page_num
    )

    history = [SingleAccessRecord(**dict(s)) for s in result]

    return HistoryResponseForm(
        msg=messages.history_response,
        records=history,
        total_pages=ceil(total / page_size),
        total_items=total,
    )
