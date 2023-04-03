class PromocodeException(Exception):
    pass


class PromocodeIsNotValid(PromocodeException):
    pass


class ItIsPersonalPromocode(PromocodeException):
    pass


class PromocodeIsSpoiled(PromocodeException):
    pass


class PromocodeIsNotFound(PromocodeException):
    pass


class MaxNumberOfActivationExceed(PromocodeException):
    pass
