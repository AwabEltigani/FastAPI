"""add table posts

Revision ID: ef173d3b638c
Revises: 
Create Date: 2025-07-20 04:50:27.406301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'ef173d3b638c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer(),unique = True,primary_key=True),
                    sa.Column("title",sa.String(50),nullable = False),
                    sa.Column("content",sa.String(255),nullable =False),
                    sa.Column("is_published",sa.Boolean(),nullable=False,default = True),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=text("now()")))



def downgrade() -> None:
    op.drop_table("posts")

