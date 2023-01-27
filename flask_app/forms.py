from __future__ import annotations

import datetime
import re
from uuid import UUID

from pydantic import BaseModel, Field, validator


class LoginForm(BaseModel):
    email: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=3, max_length=20)

    @validator("email")
    def email_valid(cls, v):
        email = v
        if (
            re.match(
                "[^@]+@[^@]+\.[^@]+",
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


class RoleForm(BaseModel):
    id: UUID = ...
    name: str = Field(min_length=3, max_length=20)
    permissions: list[str] = ...
    access_level: int = Field(default=0)


class UserRoleForm(BaseModel):
    id: UUID = ...
    user_id: UUID = ...
    role_id: UUID = ...
