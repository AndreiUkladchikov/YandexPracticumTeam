from __future__ import annotations

import datetime
from http import HTTPStatus

from pydantic import BaseModel, Field, validator

message = "msg"

already_registered = "Email is already registered"
wrong_credits = "Wrong email or password"
success_registration = "Thank you for registration!"
success_login = "Success authorization!"
bad_token = "Token has not been confirmed. Go through authorization"
success_change_credits = (
    "You have successfully changed your credentials (email or password)"
)
bad_password = "Previous password does not match"
success_refresh_tokens = "Success refreshing!"

history_response = "Here is you history"

logout_from = "Logout from "


def logout(user: str) -> str:
    return "Logout from {}".format(user)


not_allowed_resource = "This url is not allowed"


class ResponseForm(BaseModel):
    msg: str = ...


class ResponseFormWithTokens(ResponseForm):
    access_token: str = ...
    refresh_token: str = ...


class SingleAccessRecord(BaseModel):
    email: str = ...
    location: str = Field(default=None)
    device: str = Field(default=None)
    time: datetime.datetime = ...


class HistoryResponseForm(ResponseForm):
    records: list[SingleAccessRecord] | None = Field(default=None)
