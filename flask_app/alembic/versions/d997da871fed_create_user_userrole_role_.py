"""create User, UserRole, Role, UserAccessHistory tables

Revision ID: d997da871fed
Revises: 
Create Date: 2023-01-23 19:34:10.504357

"""
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision = "d997da871fed"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        ),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=True),
    )

    op.create_table(
        "roles",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("permissions", sa.ARRAY(sa.String), nullable=True),
        sa.Column("access_level", sa.Integer(), nullable=False, default=0),
    )

    op.create_table(
        "user_roles",
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "role_id",
            UUID(as_uuid=True),
            sa.ForeignKey("roles.id", ondelete="CASCADE"),
            unique=False,
            nullable=False,
        ),
    )

    op.create_table(
        "user_access_history",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("device", sa.String(), nullable=True),
        sa.Column("time", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user_access_history")
    op.drop_table("user_roles")
    op.drop_table("users")
    op.drop_table("roles")
