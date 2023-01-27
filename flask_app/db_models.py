import datetime
import enum
import uuid

from sqlalchemy import (ARRAY, Column, DateTime, ForeignKey, Integer,
                        String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from clients import postgres_client

Base = postgres_client.get_base()


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_access_in_smart" PARTITION OF "user_access_history" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_access_in_mobile" PARTITION OF "user_access_history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_access_in_web" PARTITION OF "user_access_history" FOR VALUES IN ('web')"""
    )


class User(Base):
    __tablename__ = "users"

    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, nullable=False)
    refresh_token: str = Column(String, nullable=True)
    third_party_id: str = Column(String, nullable=True)

    fk = relationship("UserRole", back_populates="fk")

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
        nullable=False,
    )

    role_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        unique=False,
        nullable=False,
    )

    fk = relationship("User", back_populates="fk")
    fk_2 = relationship("Role", back_populates="fk")

    def __repr__(self):
        return self.role_id

    def update_role(self, id):
        self.role_id = id


class Role(Base):
    __tablename__ = "roles"

    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: str = Column(String, unique=True, nullable=False)
    permissions: str = Column(ARRAY(String), nullable=True)
    access_level: int = Column(Integer, nullable=False, default=0)

    fk = relationship("UserRole", back_populates="fk_2")

    def __repr__(self):
        return self.permissions

    def update_role(self, name, permissions, access_level):
        self.name = name
        self.permissions = permissions
        self.access_level = access_level


class Action(enum.Enum):
    LOGIN = 'login'
    LOGOUT = 'logout'
    REFRESH_TOKEN = 'refresh_token'
    LOGIN_HISTORY = 'login_history'
    CHANGE_CREDITS = 'change_credits'


class UserAccessHistory(Base):
    __tablename__ = "user_access_history"
    __table_args__ = (
        UniqueConstraint('id', 'device'),
        {
            'postgresql_partition_by': 'LIST (device)',
            'listeners': [('after_create', create_partition)],
        }
    )

    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    action: str = Column(String, nullable=True)
    location: str = Column(String, nullable=True)
    device: str = Column(String, primary_key=True)
    time: datetime.datetime = Column(DateTime, nullable=False)
