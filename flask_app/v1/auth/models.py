from typing import Optional

from pydantic import BaseModel, Field


class UserInformation(BaseModel):
    id: str = ...
    default_email: str = ...
    real_name: Optional[str]
    login: Optional[str]
