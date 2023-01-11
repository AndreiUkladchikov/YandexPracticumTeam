from sqlalchemy import select, update

from base import BaseClient, BaseService
from db_models import User


class UserService(BaseService):
    def __init__(self, client: BaseClient):
        self.client = client
        self.model = User

    def all(self):
        with self.client.get_session() as session:
            users = session.scalars(select(self.model)).all()
            session.expunge_all()
            return users

    def find(self, attrs: dict):
        with self.client.get_session() as session:
            users = session.scalars(select(self.model).filter_by(**attrs)).all()
            session.expunge_all()
            return users

    def get(self, attr: dict):
        with self.client.get_session() as session:
            user = session.scalars(select(self.model).filter_by(**attr)).first()
            session.expunge_all()
            return user

    def update(self, user: User, attrs: dict):
        with self.client.get_session() as session:
            session.execute(
                update(self.model).where(self.model.id == user.id).values(**attrs)
            )

    def insert(self, user: User):
        with self.client.get_session() as session:
            session.add(user)

    def delete(self, user: User):
        with self.client.get_session() as session:
            session.delete(user)
