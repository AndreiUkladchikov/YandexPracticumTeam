from __future__ import annotations

import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

message = "msg"
successful_response = "Result successed"

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

history_response = "Here is your history"
roles_response = "Here are your roles"

logout_from = "Logout from "

user_not_found = "User by this id is not found"


def logout(user: str) -> str:
    return "Logout from {}".format(user)


not_allowed_resource = "This url is not allowed"

success_update_role = "You have successfully updated role"
success_create_role = "You have successfully created role"
success_delete_role = "You have successfully deleted role"
success_update_user_role = "You have successfully updated User role"

wrong_oauth_transaction = "You have not provided all the data for correct authorization"


class ResponseForm(BaseModel):
    msg: str = ...
    result: Any = Field(default=None)


class ResponseFormWithTokens(ResponseForm):
    access_token: str = ...
    refresh_token: str = ...


class SingleAccessRecord(BaseModel):
    email: str = ...
    location: str = Field(default=None)
    device: str = Field(default=None)
    action: str = ...
    time: datetime.datetime = ...


class HistoryResponseForm(ResponseForm):
    records: list[SingleAccessRecord] | None = Field(default=None)
    total_items: int = ...
    total_pages: int = ...


class RoleRecord(BaseModel):
    id: UUID = ...
    name: str = Field(min_length=3, max_length=20)
    permissions: list[str] = ...
    access_level: int = Field(default=0)


class RolesResponseForm(ResponseForm):
    records: list[RoleRecord] | None = Field(default=None)


class ErrorYandexResponseForm(BaseModel):
    error_description: Optional[str]
    error: Optional[str]


class UserExtended(BaseModel):
    user_id: UUID
    email: str
    first_name: str | None
    last_name: str | None


class GetALlUsers(BaseModel):
    result: list[UserExtended] | None
