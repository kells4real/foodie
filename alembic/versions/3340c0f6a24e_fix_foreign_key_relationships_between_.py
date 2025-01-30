"""Fix foreign key relationships between order and order_items

Revision ID: 3340c0f6a24e
Revises: 75c0d5516858
Create Date: 2025-01-30 03:19:42.999520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3340c0f6a24e'
down_revision: Union[str, None] = '75c0d5516858'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
