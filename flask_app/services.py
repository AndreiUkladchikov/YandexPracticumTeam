from sqlalchemy import select, update

from base import BaseClient, BaseService
from db_models import User, Role, UserAccessHistory, UserRole


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


class AccessHistoryService(BaseService):
    def __init__(self, client: BaseClient):
        self.client = client
        self.model = UserAccessHistory

    def all(self) -> list[UserAccessHistory]:
        with self.client.get_session() as session:
            users = session.scalars(select(self.model)).all()
            session.expunge_all()
            return users

    def find(self, attrs: dict) -> list[UserAccessHistory]:
        with self.client.get_session() as session:
            users = session.scalars(select(self.model).filter_by(**attrs)).all()
            session.expunge_all()
            return users

    def get(self, attr: dict) -> UserAccessHistory:
        with self.client.get_session() as session:
            user_access_history = session.scalars(select(self.model).filter_by(**attr)).first()
            session.expunge_all()
            return user_access_history

    def update(self, user_access_history: UserAccessHistory, attrs: dict):
        with self.client.get_session() as session:
            session.execute(
                update(self.model).where(self.model.id == user_access_history.id).values(**attrs)
            )

    def insert(self, user_access_history: UserAccessHistory):
        with self.client.get_session() as session:
            session.add(user_access_history)

    def delete(self, user_access_history: UserAccessHistory):
        with self.client.get_session() as session:
            session.delete(user_access_history)

    def clear(self):
        with self.client.get_session() as session:
            session.query(UserAccessHistory).delete()


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

    def insert(self, roles: Role):
        with self.client.get_session() as session:
            session.add(roles)

    def delete(self, roles: Role):
        with self.client.get_session() as session:
            session.delete(roles)

    def clear(self):
        with self.client.get_session() as session:
            session.query(Role).delete()


class UserRoleService(BaseService):
    def __init__(self, client: BaseClient):
        self.client = client
        self.model = UserRole

    def all(self) -> list[UserRole]:
        with self.client.get_session() as session:
            user_role = session.scalars(select(self.model)).all()
            session.expunge_all()
            return user_role

    def find(self, attrs: dict) -> list[UserRole]:
        with self.client.get_session() as session:
            user_role = session.scalars(select(self.model).filter_by(**attrs)).all()
            session.expunge_all()
            return user_role

    def get(self, attr: dict) -> UserRole:
        with self.client.get_session() as session:
            user_role = session.scalars(select(self.model).filter_by(**attr)).first()
            session.expunge_all()
            return user_role

    def update(self, user_role: UserRole, attrs: dict):
        with self.client.get_session() as session:
            session.execute(
                update(self.model).where(self.model.id == user_role.id).values(**attrs)
            )

    def insert(self, user_role: UserRole):
        with self.client.get_session() as session:
            session.add(user_role)

    def delete(self, user_role: UserRole):
        with self.client.get_session() as session:
            session.delete(user_role)

    def clear(self):
        with self.client.get_session() as session:
            session.query(UserRole).delete()
