from sqlalchemy import select, update

from base import BaseClient, BaseService
from db_models import User, Role


class UserService(BaseService):
    def __init__(self, client: BaseClient):
        self.client = client
        self.model = User

    def all(self) -> list[User]:
        with self.client.get_session() as session:
            users = session.scalars(select(self.model)).all()
            session.expunge_all()
            return users

    def find(self, attrs: dict) -> list[User]:
        with self.client.get_session() as session:
            users = session.scalars(select(self.model).filter_by(**attrs)).all()
            session.expunge_all()
            return users

    def get(self, attr: dict) -> User:
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

    def clear(self):
        with self.client.get_session() as session:
            session.query(User).delete()


class RoleService(BaseService):
    def __init__(self, client: BaseClient):
        self.client = client
        self.model = Role

    def all(self) -> list[Role]:
        with self.client.get_session() as session:
            roles = session.scalars(select(self.model)).all()
            session.expunge_all()
            return roles

    def find(self, attrs: dict) -> list[Role]:
        with self.client.get_session() as session:
            roles = session.scalars(select(self.model).filter_by(**attrs)).all()
            session.expunge_all()
            return roles

    def get(self, attr: dict) -> Role:
        with self.client.get_session() as session:
            role = session.scalars(select(self.model).filter_by(**attr)).first()
            session.expunge_all()
            return role

    def update(self, user: Role, attrs: dict):
        with self.client.get_session() as session:
            session.execute(
                update(self.model).where(self.model.id == user.id).values(**attrs)
            )

    def insert(self, user: Role):
        with self.client.get_session() as session:
            session.add(user)

    def delete(self, user: Role):
        with self.client.get_session() as session:
            session.delete(user)

    def clear(self):
        with self.client.get_session() as session:
            session.query(Role).delete()
