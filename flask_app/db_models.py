import uuid
import datetime

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from flask_app.clients import postgres_client

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
    email: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    refresh: str = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id: uuid.UUID = db.Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        nullable=False,
    )

    role_id: uuid.UUID = db.Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    def __repr__(self):
        return self.role_id

    def update_role(self, id):
        self.role_id = id


class Role(db.Model):
    __tablename__ = "roles"

    id: uuid.UUID = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: str = db.Column(db.String, unique=True, nullable=False)
    permissions: str = db.Column(db.String, nullable=True)
    access_level: int = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return self.permissions

    def update_role(self, name, permissions, access_level):
        self.name = name
        self.permissions = permissions
        self.access_level = access_level


class UserAccessHistory(db.Model):
    __tablename__ = "user_access_history"

    id: int = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id: uuid.UUID = db.Column(
        UUID(as_uuid=True),
        nullable=False,
    )

    location: str = db.Column(db.String, nullable=False)
    device: str = db.Column(db.String, nullable=False)
    time: datetime.datetime = db.Column(db.DateTime, nullable=False)
