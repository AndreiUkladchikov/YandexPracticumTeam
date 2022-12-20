import abc


class DbProtocol():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    async def _get_by_id(index: str, id: str):
        pass

    @abc.abstractmethod
    async def _close():
        pass
