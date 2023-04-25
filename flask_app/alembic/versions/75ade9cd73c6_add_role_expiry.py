"""Add role expiry

Revision ID: 75ade9cd73c6
Revises: 897dfea3c5d9
Create Date: 2023-04-01 10:28:35.538513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75ade9cd73c6'
down_revision = '897dfea3c5d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(op.f("uq_user_roles_user_id"), "user_roles", type_="unique")
    op.add_column("user_roles", sa.Column("expiry_date", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_user_roles_user_id"), "user_roles", ["user_id"]
    )
    op.drop_column("user_roles", "expiry_date")
