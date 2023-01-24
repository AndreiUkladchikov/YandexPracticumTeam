import http
from urllib.parse import urlencode

import requests
from flask import Blueprint, redirect, request
from flask_jwt_extended import create_access_token, create_refresh_token
from loguru import logger
from pydantic import ValidationError
from spectree import Response

import messages
from config import settings
from db_models import User, UserRole
from documentation import spec
from helpers import generate_password
from messages import (ErrorYandexResponseForm, ResponseForm,
                      ResponseFormWithTokens)
from services import role_service, user_role_service, user_service
from v1.auth.models import UserInformation

oauth_blueprint = Blueprint("oauth", __name__)

baseurl = "https://oauth.yandex.ru/"
login_url_yandex = "https://login.yandex.ru/info/"


@oauth_blueprint.route("/oauth-login", methods=["GET"])
@spec.validate(
    resp=Response(HTTP_200=ResponseFormWithTokens, HTTP_401=ErrorYandexResponseForm),
    tags=["OAuth2"],
)
def oauth_login():
    if request.args.get("code", False):
        # Если скрипт был вызван с указанием параметра "code" в URL,
        # то выполняется запрос на получение токена
        logger.info(request.args)
        logger.info(request.data)
        data = {
            "grant_type": "authorization_code",
            "code": request.args.get("code"),
            "client_id": settings.oauth_client_id,
            "client_secret": settings.oauth_client_secret,
        }
        data = urlencode(data)
        result = requests.post(baseurl + "token", data)

        if result.status_code == http.HTTPStatus.OK:
            access_token_oauth = result.json()["access_token"]
            refresh_token_oauth = result.json()["refresh_token"]

            headers = {"Authorization": f"Bearer {access_token_oauth}"}
            data = {"format": "json"}

            response = requests.get(login_url_yandex, data=data, headers=headers)
            logger.info(response.json())
            try:
                user_info = UserInformation(**response.json())
            except ValidationError:
                return ResponseForm(msg=messages.wrong_oauth_transaction)

            user_from_db = user_service.get({"email": user_info.default_email})

            access_token = create_access_token(identity=user_info.default_email)
            refresh_token = create_refresh_token(identity=user_info.default_email)

            if not user_from_db:
                new_user = User(email=user_info.default_email)

                new_user.third_party_id = user_info.id

                password = generate_password()
                new_user.set_password(password)

                new_user.refresh_token = refresh_token

                user_service.insert(new_user)

                u = user_service.get({"email": user_info.default_email})
                role = role_service.get({"name": "subscriber"})
                user_role = UserRole(user_id=u.id, role_id=role.id)

                user_role_service.insert(user_role)

            return ResponseFormWithTokens(
                msg=messages.success_login,
                access_token=access_token,
                refresh_token=refresh_token,
            )

        return ErrorYandexResponseForm(**result.json())

    else:
        # Если скрипт был вызван без указания параметра "code",
        # то пользователь перенаправляется на страницу запроса доступа

        return redirect(
            baseurl
            + "authorize?response_type=code&client_id={}".format(
                settings.oauth_client_id
            )
        )
