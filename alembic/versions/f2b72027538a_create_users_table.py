"""create users table

Revision ID: f2b72027538a
Revises: ef173d3b638c
Create Date: 2025-07-20 05:01:16.808672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'f2b72027538a'
down_revision: Union[str, Sequence[str], None] = 'ef173d3b638c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer(),primary_key=True),
                    sa.Column("email",sa.String(255),nullable = False),
                    sa.Column("password",sa.String(50),nullable = False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),default = text("now()"))
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
