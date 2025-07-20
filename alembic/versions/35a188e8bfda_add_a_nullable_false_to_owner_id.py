"""add a nullable = false to owner_id

Revision ID: 35a188e8bfda
Revises: a6bcb3a7572b
Create Date: 2025-07-20 05:38:38.816685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35a188e8bfda'
down_revision: Union[str, Sequence[str], None] = 'a6bcb3a7572b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("posts","owner_id",nullable=False)
    pass


def downgrade() -> None:
    op.alter_column("posts","owner_id",nullable=True)
    pass
