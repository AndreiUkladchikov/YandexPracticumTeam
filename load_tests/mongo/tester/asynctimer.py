import asyncio
import time

from loguru import logger


def timeit(func):

    async def helper(*args, **params):
        logger.info(f'Start timeit for {func.__name__}.')
        _results = []
        for _ in range(100):
            start = time.time()
            result = await func(*args, **params)
            _results.append(time.time() - start)
        logger.info(
            f'{func.__name__} results: max: {max(_results)}, min: {min(_results)}, avg: {sum(_results)/len(_results)}'
        )
        return result

    return helper
