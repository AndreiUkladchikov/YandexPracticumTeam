from functools import wraps
from time import monotonic_ns

import aiohttp
import pydantic.error_wrappers
from async_lru import alru_cache
from src.config import settings
from src.custom_log import logger
from src.schemas import Film


def timed_lru_cache(
    _func=None,
    *,
    seconds: int = settings.time_cache_expired,
    maxsize: int = 128,
    typed: bool = False
):
    """Extension over existing lru_cache with timeout
    :param seconds: timeout value
    :param maxsize: maximum size of the cache
    :param typed: whether different keys for different types of cache keys
    """

    def wrapper_cache(f):
        # create a function wrapped with traditional lru_cache
        f = alru_cache(maxsize=maxsize, typed=typed)(f)
        # convert seconds to nanoseconds to set the expiry time in nanoseconds
        f.delta = seconds * 10**9
        f.expiration = monotonic_ns() + f.delta

        @wraps(f)  # wraps is used to access the decorated function attributes
        def wrapped_f(*args, **kwargs):
            if monotonic_ns() >= f.expiration:
                # if the current cache expired of the decorated function then
                # clear cache for that function and set a new cache value with new expiration time
                f.cache_clear()
                f.expiration = monotonic_ns() + f.delta
            return f(*args, **kwargs)

        wrapped_f.cache_info = f.cache_info
        wrapped_f.cache_clear = f.cache_clear
        return wrapped_f

    # To allow decorator to be used without arguments
    if _func is None:
        return wrapper_cache
    else:
        return wrapper_cache(_func)


@timed_lru_cache(maxsize=10)
async def get_data_from_film_service(film_id: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://{}:{}/api/v1/films/{}".format(
                    settings.film_service_host, settings.film_service_port, film_id
                )
            ) as resp:
                film = await resp.json()
                return Film(**film)
    except pydantic.error_wrappers.ValidationError:
        logger.error({**film, **{"msg": "From FilmService"}})
    except aiohttp.client_exceptions.ClientConnectorError as ce:
        logger.error(ce)
