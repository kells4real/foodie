"""Fix foreign key references

Revision ID: 786f3a11cb4e
Revises: dcbdc80b7bab
Create Date: 2025-01-30 03:02:34.943185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '786f3a11cb4e'
down_revision: Union[str, None] = 'dcbdc80b7bab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
