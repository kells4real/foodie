"""Initial migration

Revision ID: 9b10e8d5cf50
Revises: 581a013156f8
Create Date: 2025-01-30 03:06:52.623536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b10e8d5cf50'
down_revision: Union[str, None] = '581a013156f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
