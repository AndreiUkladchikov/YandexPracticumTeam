import datetime
import uuid

from sqlalchemy import (ARRAY, Column, DateTime, ForeignKey, Integer, MetaData,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from clients import postgres_client

Base = postgres_client.get_base()


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


class UserAccessHistory(Base):
    __tablename__ = "user_access_history"

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

    location: str = Column(String, nullable=True)
    device: str = Column(String, nullable=True)
    time: datetime.datetime = Column(DateTime, nullable=False)
