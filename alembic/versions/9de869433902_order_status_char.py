"""order status char

Revision ID: 9de869433902
Revises: 9b10e8d5cf50
Create Date: 2025-01-30 03:10:08.721092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9de869433902'
down_revision: Union[str, None] = '9b10e8d5cf50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
