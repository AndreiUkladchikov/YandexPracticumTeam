import abc
from abc import ABC

from flask_sqlalchemy.model import Model


class BaseClient(ABC):
    @abc.abstractmethod
    def get_session(self):
        pass


class BaseService(ABC):
    client = BaseClient
    model = None

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def find(self, attrs: dict):
        pass

    @abc.abstractmethod
    def get(self, attr: dict):
        pass

    @abc.abstractmethod
    def update(self, obj: Model, attrs: dict):
        pass

    @abc.abstractmethod
    def insert(self, obj: Model):
        pass

    @abc.abstractmethod
    def delete(self, obj: Model):
        pass

    @abc.abstractmethod
    def clear(self):
        pass
