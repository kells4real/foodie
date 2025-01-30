"""Initial migration

Revision ID: d3d55629a8ec
Revises: a01de85ab32c
Create Date: 2025-01-30 02:54:25.243605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3d55629a8ec'
down_revision: Union[str, None] = 'a01de85ab32c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
