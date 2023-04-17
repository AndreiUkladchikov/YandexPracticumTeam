class PromocodeException(Exception):
    pass


class PromocodeIsNotValid(PromocodeException):
    def __init__(self, promocode_id):
        self.promocode_id = promocode_id

        super().__init__("Promocode exists but Not Valid! " f"Promo id {promocode_id}")


class ItIsPersonalPromocode(PromocodeException):
    def __init__(self, promocode_id):
        self.promocode_id = promocode_id

        super().__init__("It Is Personal Promocode! " f"Promo id {promocode_id}")


class PromocodeIsSpoiled(PromocodeException):
    def __init__(self, promocode_id):
        self.promocode_id = promocode_id

        super().__init__("Promocode is Not Valid! " f"Promo id: {promocode_id}")


class PromocodeIsNotFound(PromocodeException):
    def __init__(self, promo_value):
        self.promo_value = promo_value

        super().__init__("Promocode Is Not Found! " f"Promo value {promo_value}")


class MaxNumberOfActivationExceed(PromocodeException):
    def __init__(self, promocode_id):
        self.promocode_id = promocode_id

        super().__init__("Max Number Of Activation Exceed! " f"Promo id {promocode_id}")


class UserIsNotInUserHistory(PromocodeException):
    def __init__(self, user_id):
        self.user_id = user_id

        super().__init__("User is not in user history! " f"User id {user_id}")


class PromocodeAlreadyActivatedByCurrentUser(PromocodeException):
    def __init__(self, user_id, promo_id):
        self.user_id = user_id
        self.promocode_id = promo_id

        super().__init__(
            "Promocode has been already activated! "
            f"User id {user_id}, promocode id {promo_id}"
        )
