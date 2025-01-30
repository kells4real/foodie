"""Initial migration

Revision ID: 5222d15cc028
Revises: 786f3a11cb4e
Create Date: 2025-01-30 03:03:36.727143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5222d15cc028'
down_revision: Union[str, None] = '786f3a11cb4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
