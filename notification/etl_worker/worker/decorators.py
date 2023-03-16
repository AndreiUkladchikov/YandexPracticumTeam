import re
from functools import wraps
from time import sleep

from config import settings
from loguru import logger


def backoff(
    start_sleep_time: float = settings.backoff_start_sleep_time,
    factor: int = settings.backoff_factor,
    border_sleep_time: float = settings.backoff_border_sleep_time,
    try_limit: int = settings.backoff_try_limit,
):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor)
    до граничного времени ожидания (border_sleep_time).
    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param try_limit: кол-во попыток после достижения border_sleep_time
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            def retry(factor: int, try_number: int = 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    t: float = start_sleep_time * 2**factor
                    wait: float = t if t < border_sleep_time else border_sleep_time
                    try_number: int = 1 if t < border_sleep_time else try_number + 1
                    mes = f"""Try #{factor-1}. Exception "{e}" was raised when execute function "{func.__name__}". \
                               Wait for {wait} second(s)."""
                    logger.error("".join(re.sub(" +", " ", mes).splitlines()))
                    sleep(wait)
                    if try_number <= try_limit:
                        return retry(factor + 1, try_number)
                    else:
                        try_limit_error_mes = f'Function "{func.__name__}" reached the limit of attempts.'
                        logger.error(try_limit_error_mes)
                        raise Exception(try_limit_error_mes)

            return retry(factor)

        return inner

    return func_wrapper
