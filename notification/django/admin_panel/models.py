import uuid
from enum import Enum

from django.db import models


class MessageModel():
    type = str
    subject = str
    template = str
    user_id = uuid.UUID
    film_id = uuid.UUID | None


class MessageTypes(Enum):
    AUTH = 'AUTH'
    MASS_DELIVERY = 'MASS'
    UGC = 'UGC'
