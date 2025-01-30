"""Add length to menu name column

Revision ID: 581a013156f8
Revises: 5222d15cc028
Create Date: 2025-01-30 03:05:37.041025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '581a013156f8'
down_revision: Union[str, None] = '5222d15cc028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
