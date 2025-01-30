"""Initial migration

Revision ID: dcbdc80b7bab
Revises: d3d55629a8ec
Create Date: 2025-01-30 02:59:03.383146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcbdc80b7bab'
down_revision: Union[str, None] = 'd3d55629a8ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
