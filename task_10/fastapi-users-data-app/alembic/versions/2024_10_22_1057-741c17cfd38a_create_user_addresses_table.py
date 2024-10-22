"""Create user addresses table

Revision ID: 741c17cfd38a
Revises: 84266b31536e
Create Date: 2024-10-22 10:57:19.383617

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "741c17cfd38a"
down_revision: Union[str, None] = "84266b31536e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("street", sa.String(), nullable=False),
        sa.Column("suite", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("zipcode", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_addresses_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_addresses")),
        sa.UniqueConstraint("user_id", name=op.f("uq_user_addresses_user_id")),
    )


def downgrade() -> None:
    op.drop_table("user_addresses")
