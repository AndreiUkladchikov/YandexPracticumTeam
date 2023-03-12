from enum import Enum

from django.db import models


class MessageTypes(Enum):
    AUTH = 'AUTH'
    MASS_DELIVERY = 'MASS'
    UGC = 'UGC'
