from __future__ import annotations

import datetime
from pydantic import BaseModel, Field, validator

message = "msg"

already_registered = {message: "Email is already registered"}
wrong_credits = {message: "Wrong email or password"}
success_registration = {message: "Thank you for registration!"}
bad_token = {message: "Token has not been confirmed. Go through authorization"}
success_change_credits = {message: "You have successfully changed your credentials (email or password)"}
bad_password = {message: "Previous password does not match"}

history_response = {message: "Here is you history"}

not_allowed_resource = {message: "This url is not allowed"}


class ResponseForm(BaseModel):
    msg: str = ...


class SingleAccessRecord(BaseModel):
    email: str = ...
    location: str = Field(default=None)
    device: str = Field(default=None)
    time: datetime.datetime = ...


class HistoryResponseForm(ResponseForm):
    msg: str = ...
    records: list[SingleAccessRecord] | None = Field(default=None)
