"""Add partitions

Revision ID: b128430e7a88
Revises: 3a553fb8b911
Create Date: 2023-01-27 20:49:55.953687

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b128430e7a88"
down_revision = "3a553fb8b911"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "uq_user_access_history_id", "user_access_history", type_="unique"
    )
    op.create_unique_constraint(
        op.f("uq_user_access_history_id"), "user_access_history", ["id", "device"]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("uq_user_access_history_id"), "user_access_history", type_="unique"
    )
    op.create_unique_constraint(
        "uq_user_access_history_id", "user_access_history", ["id"]
    )
    # ### end Alembic commands ###
