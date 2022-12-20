import abc


class CacheProtocol():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    async def _get():
        pass

    @abc.abstractmethod
    async def _put():
        pass

    @abc.abstractmethod
    async def _close():
        pass
