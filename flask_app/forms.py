from __future__ import annotations

import datetime
import re

from pydantic import BaseModel, Field, validator


class LoginForm(BaseModel):
    email: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=3, max_length=20)

    @validator("email")
    def email_valid(cls, v):
        email = v.lower()
        if (
            re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                email,
            )
            is None
        ):
            raise ValueError("The provided email address is invalid")
        return email


class PasswordResetForm(LoginForm):
    previous_password: str = Field(min_length=3, max_length=20)


class SingleAccessRecord(BaseModel):
    email: str = ...
    location: str = Field(default=None)
    device: str = Field(default=None)
    time: datetime.datetime = ...


class HistoryResponseForm(BaseModel):
    msg: str = ...
    records: list[SingleAccessRecord] | None = Field(default=None)
