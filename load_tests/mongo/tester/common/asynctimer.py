import time

from loguru import logger

from common.config import settings


def timeit(func):
    """Вычисляем время выполнения функции. 

    Находим худшее, лучшее и среднее время выполнения функции,
    при кол-ве вызов указанном в ENV переменной timeit_func_call_count.
    """
    async def helper(*args, **params):
        logger.info(f'Start timeit for {func.__name__}.')
        _results = []
        for _ in range(settings.timeit_func_call_count):
            start = time.time()
            result = await func(*args, **params)
            _results.append(time.time() - start)
        logger.info(
            f'{func.__name__} results: max: {max(_results)}, min: {min(_results)}, avg: {sum(_results)/len(_results)}'
        )
        return result

    return helper
