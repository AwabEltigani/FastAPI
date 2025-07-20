"""add foriegn key to posts table

Revision ID: a6bcb3a7572b
Revises: ed2f408b3c4c
Create Date: 2025-07-20 05:12:36.423623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6bcb3a7572b'
down_revision: Union[str, Sequence[str], None] = 'ed2f408b3c4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable = True))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk","posts")
    op.drop_column("owner_id","posts")
    pass
