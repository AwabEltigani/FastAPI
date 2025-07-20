"""create default constraint for the created_at column in users

Revision ID: ed2f408b3c4c
Revises: f2b72027538a
Create Date: 2025-07-20 05:07:23.984770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'ed2f408b3c4c'
down_revision: Union[str, Sequence[str], None] = 'f2b72027538a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users","created_at",server_default = sa.text("now()"))
    pass


def downgrade() -> None:
    op.alter_column("users", "created_at")
    pass
