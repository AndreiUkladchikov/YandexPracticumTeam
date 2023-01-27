from sqlalchemy import select, update

from clients import postgres_client

from sqlalchemy import func

from base import BaseClient, BaseService
from db_models import Base, Role, User, UserAccessHistory, UserRole


class CustomService(BaseService):
    def __init__(self, client: BaseClient, model: Base = None):
        self.client = client
        if model:
            self.model = model

    def all(self) -> list[Base]:
        with self.client.get_session() as session:
            objs = session.scalars(select(self.model)).all()
            session.expunge_all()
            return objs

    def find(self, attrs: dict) -> list[Base]:
        with self.client.get_session() as session:
            objs = session.scalars(select(self.model).filter_by(**attrs)).all()
            session.expunge_all()
            return objs

    def get(self, attr: dict) -> Base:
        with self.client.get_session() as session:
            obj = session.scalars(select(self.model).filter_by(**attr)).first()
            session.expunge_all()
            return obj

    def update(self, obj: Base, attrs: dict):
        with self.client.get_session() as session:
            session.execute(
                update(self.model).where(self.model.id == obj.id).values(**attrs)
            )

    def insert(self, obj: Base):
        with self.client.get_session() as session:
            session.add(obj)

    def delete(self, obj: Base):
        with self.client.get_session() as session:
            session.delete(obj)

    def clear(self):
        with self.client.get_session() as session:
            session.query(self.model).delete()


class AccessHistoryService(CustomService):
    model = UserAccessHistory

    def get_detailed_info_about(self, user: User, page_size: int, page_num: int):
        with self.client.get_session() as session:
            result = (
                session.query(
                    User.email,
                    self.model.location,
                    self.model.device,
                    self.model.time,
                    self.model.action
                )
                .join(self.model, User.id == self.model.user_id)
                .filter(User.email == user.email)
                .slice((page_num - 1) * page_size, page_num * page_size)
                .all()
            )
            total = session.query(func.count(self.model.id)).filter(self.model.user_id == user.id).scalar()
            session.expunge_all()
            return result, total


class UserRoleService(CustomService):
    model = UserRole

    def get_permissions_of(self, user: User):
        with self.client.get_session() as session:
            permissions = (
                session.query(Role.permissions)
                .join(self.model, Role.id == self.model.role_id)
                .join(User, User.id == self.model.user_id)
                .filter(User.email == user)
                .one_or_none()
            )
            session.expunge_all()
            return permissions


user_service = CustomService(client=postgres_client, model=User)
role_service = CustomService(client=postgres_client, model=Role)
access_history_service = AccessHistoryService(postgres_client)
user_role_service = UserRoleService(postgres_client)
