"""Add column third_party_id to users

Revision ID: 326d8fad876f
Revises: d997da871fed
Create Date: 2023-01-24 19:02:14.452860

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "326d8fad876f"
down_revision = "d997da871fed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("third_party_id", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "third_party_id")
